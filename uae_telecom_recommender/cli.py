"""
Command Line Interface for UAE Telecom Recommender System.
"""

import click
import json
from typing import Optional
from datetime import datetime

from .core.recommender import TelecomRecommenderSystem
from .sectors.base_sector import ProjectData


@click.group()
@click.version_option(version="0.1.0")
def cli():
    """UAE Telecom Recommender System CLI
    
    Sector-aware recommender system for project risk management 
    in UAE telecom infrastructure.
    """
    pass


@cli.command()
@click.option('--project-id', required=True, help='Project identifier')
@click.option('--description', required=True, help='Project description')
@click.option('--budget', type=float, required=True, help='Project budget in AED')
@click.option('--timeline-days', type=int, required=True, help='Project timeline in days')
@click.option('--complexity', type=float, default=0.5, help='Complexity score (0.0-1.0)')
@click.option('--technologies', help='Comma-separated list of technologies')
@click.option('--stakeholders', help='Comma-separated list of stakeholders')
@click.option('--dependencies', help='Comma-separated list of dependencies')
@click.option('--sectors', help='Comma-separated list of sectors to assess')
@click.option('--output', type=click.Choice(['json', 'summary']), default='summary', help='Output format')
def assess(project_id: str, description: str, budget: float, timeline_days: int,
          complexity: float, technologies: Optional[str], stakeholders: Optional[str],
          dependencies: Optional[str], sectors: Optional[str], output: str):
    """Assess project risk across all relevant sectors."""
    
    try:
        # Initialize the recommender system
        recommender = TelecomRecommenderSystem()
        
        # Parse comma-separated inputs
        tech_list = technologies.split(',') if technologies else ['General IT']
        stakeholder_list = stakeholders.split(',') if stakeholders else ['Project Team']
        dependency_list = dependencies.split(',') if dependencies else []
        sector_filter = sectors.split(',') if sectors else None
        
        # Create project data
        project_data = ProjectData(
            project_id=project_id,
            sector_id="general",  # Will be determined by assessment
            description=description,
            budget=budget,
            timeline_days=timeline_days,
            complexity_score=complexity,
            stakeholders=[s.strip() for s in stakeholder_list],
            technologies=[t.strip() for t in tech_list],
            dependencies=[d.strip() for d in dependency_list]
        )
        
        # Conduct assessment
        report = recommender.assess_project(project_data, sector_filter)
        
        if output == 'json':
            click.echo(report.to_json())
        else:
            _print_summary_report(report)
            
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise click.Abort()


@cli.command()
@click.option('--project-type', 
              type=click.Choice(['network_upgrade', 'cybersecurity_enhancement', 'customer_portal']),
              default='network_upgrade',
              help='Type of sample project')
@click.option('--output', type=click.Choice(['json', 'summary']), default='summary', help='Output format')
def sample(project_type: str, output: str):
    """Run assessment on a sample project."""
    
    try:
        recommender = TelecomRecommenderSystem()
        
        # Create sample project
        project_data = recommender.create_sample_project(project_type)
        
        # Conduct assessment
        report = recommender.assess_project(project_data)
        
        click.echo(f"Sample Project Assessment: {project_type.replace('_', ' ').title()}")
        click.echo("=" * 60)
        
        if output == 'json':
            click.echo(report.to_json())
        else:
            _print_summary_report(report)
            
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise click.Abort()


@cli.command()
def sectors():
    """List all available sectors and their information."""
    
    try:
        recommender = TelecomRecommenderSystem()
        sector_info = recommender.get_sector_information()
        
        click.echo("UAE Telecom Sectors")
        click.echo("=" * 50)
        
        for sector_id, info in sector_info.items():
            status = "✓ Implemented" if info['implemented'] else "⚠ Placeholder"
            click.echo(f"\n{info['name']} ({sector_id})")
            click.echo(f"  Status: {status}")
            click.echo(f"  Weight: {info['weight']:.1%}")
            click.echo(f"  Description: {info['description']}")
            click.echo(f"  Risk Factors: {info['risk_factors_count']}")
            
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise click.Abort()


@cli.command()
def context():
    """Show UAE telecom regulatory and business context."""
    
    try:
        recommender = TelecomRecommenderSystem()
        uae_context = recommender.get_uae_context()
        
        click.echo("UAE Telecom Context")
        click.echo("=" * 50)
        
        # Regulatory environment
        reg_env = uae_context['regulatory_environment']
        click.echo(f"\nPrimary Regulator: {reg_env['primary_regulator']}")
        click.echo("\nKey Legal Frameworks:")
        for law in reg_env['key_laws']:
            click.echo(f"  • {law}")
            
        click.echo("\nEmergency Contacts:")
        for contact in reg_env['emergency_contacts']:
            click.echo(f"  • {contact}")
        
        # Risk tolerance
        click.echo(f"\nRisk Tolerance Levels:")
        for level, threshold in uae_context['risk_tolerance'].items():
            click.echo(f"  • {level.title()}: {threshold:.1%}")
        
        # Sectors overview
        click.echo(f"\nSector Weights:")
        sectors = uae_context['sectors_overview']
        for sector_id, info in sorted(sectors.items(), key=lambda x: x[1]['weight'], reverse=True):
            click.echo(f"  • {info['name']}: {info['weight']:.1%}")
            
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise click.Abort()


def _print_summary_report(report):
    """Print a formatted summary report."""
    
    # Header
    click.echo(f"\nProject: {report.project_data.project_id}")
    click.echo(f"Generated: {report.generated_at}")
    click.echo("=" * 60)
    
    # Overall risk
    risk_color = _get_risk_color(report.overall_risk)
    click.echo(f"\nOverall Risk Level: ", nl=False)
    click.secho(f"{report.overall_risk:.1%} ({report.risk_category})", 
               fg=risk_color, bold=True)
    
    # Risk bar visualization
    bar_length = 20
    filled_length = int(bar_length * report.overall_risk)
    bar = "█" * filled_length + "░" * (bar_length - filled_length)
    click.echo(f"Risk Bar: [{bar}]")
    
    # Sector assessments
    click.echo(f"\nSector Risk Assessment:")
    click.echo("-" * 30)
    
    for sector_id, assessment in report.risk_assessments.items():
        risk_color = _get_risk_color(assessment.risk_level)
        click.echo(f"{sector_id.replace('_', ' ').title():<25}", nl=False)
        click.secho(f"{assessment.risk_level:.1%}", fg=risk_color, bold=True)
        
        # Show top risk factors for this sector
        if assessment.risk_factors:
            click.echo(f"  Risk Factors: {', '.join(assessment.risk_factors[:3])}")
    
    # Top risk factors across all sectors
    if report.top_risks:
        click.echo(f"\nTop Risk Factors:")
        click.echo("-" * 20)
        for i, (factor, sector, risk_level) in enumerate(report.top_risks[:5], 1):
            risk_color = _get_risk_color(risk_level)
            click.echo(f"{i}. {factor} ", nl=False)
            click.secho(f"({sector}, {risk_level:.1%})", fg=risk_color)
    
    # Priority recommendations
    if report.priority_recommendations:
        click.echo(f"\nPriority Recommendations:")
        click.echo("-" * 30)
        for i, (recommendation, sector, risk_level) in enumerate(report.priority_recommendations[:8], 1):
            click.echo(f"{i}. {recommendation}")
            click.echo(f"   → {sector} (Risk: {risk_level:.1%})")
    
    # UAE-specific guidance
    click.echo(f"\nUAE Regulatory Guidance:")
    click.echo("-" * 25)
    
    if report.overall_risk > 0.7:
        click.echo("• Contact UAE Telecommunications Regulatory Authority (TRA)")
        click.echo("• Consider engaging UAE cybersecurity consultants")
        click.echo("• Review compliance with UAE Cyber Security Law")
    elif report.overall_risk > 0.4:
        click.echo("• Ensure compliance monitoring is in place")
        click.echo("• Consider periodic regulatory reviews")
    else:
        click.echo("• Maintain standard compliance procedures")
        click.echo("• Continue monitoring regulatory updates")


def _get_risk_color(risk_level: float) -> str:
    """Get color code for risk level visualization."""
    if risk_level >= 0.8:
        return 'red'
    elif risk_level >= 0.6:
        return 'yellow'
    elif risk_level >= 0.4:
        return 'cyan'
    else:
        return 'green'


def main():
    """Main entry point for the CLI."""
    cli()


if __name__ == '__main__':
    main()