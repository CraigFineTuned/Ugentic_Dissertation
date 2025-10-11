# Agent_ServerInfra - IT Server Infrastructure AI Agent
# UGENTIC Framework - Departmental AI Agent
# Ubuntu Principle: "I am because we are" - Infrastructure exists to serve the collective

from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import logging
from datetime import datetime, timedelta
import json

class InfrastructureComponent(Enum):
    """Infrastructure components based on real IT operations"""
    WEB_SERVER = "web_server"
    DATABASE_SERVER = "database_server"
    FILE_SERVER = "file_server"
    DOMAIN_CONTROLLER = "domain_controller"
    BACKUP_SYSTEM = "backup_system"
    NETWORK_SWITCH = "network_switch"
    FIREWALL = "firewall"
    LOAD_BALANCER = "load_balancer"
    STORAGE_ARRAY = "storage_array"

class SystemHealth(Enum):
    """System health status levels"""
    OPTIMAL = "optimal"          # 95-100% performance
    GOOD = "good"               # 85-94% performance
    WARNING = "warning"         # 70-84% performance
    CRITICAL = "critical"       # Below 70% performance
    DOWN = "down"               # System unavailable

class MaintenanceType(Enum):
    """Types of maintenance operations"""
    PREVENTIVE = "preventive"           # Scheduled regular maintenance
    CORRECTIVE = "corrective"          # Fix identified issues
    ADAPTIVE = "adaptive"              # Improve performance/capacity
    EMERGENCY = "emergency"            # Critical issue response
    SECURITY_UPDATE = "security_update" # Security patches and updates

@dataclass
class InfrastructureAlert:
    """Infrastructure monitoring alert structure"""
    alert_id: str
    component: InfrastructureComponent
    severity: SystemHealth
    description: str
    timestamp: datetime
    threshold_exceeded: Optional[str] = None
    impact_assessment: Optional[str] = None
    ubuntu_collective_impact: bool = False  # Affects multiple departments
    suggested_response: Optional[str] = None

@dataclass
class MaintenanceWindow:
    """Maintenance window planning structure"""
    maintenance_id: str
    components: List[InfrastructureComponent]
    maintenance_type: MaintenanceType
    planned_start: datetime
    estimated_duration: int  # minutes
    business_impact: str
    affected_departments: List[str]
    ubuntu_coordination_required: bool = True  # Always coordinate with collective

class Agent_ServerInfra:
    """
    IT Server Infrastructure AI Agent
    
    Behavioral Patterns Based on Real Department Analysis:
    - Proactive monitoring and preventive action
    - Strategic long-term thinking balanced with immediate response
    - Deep technical expertise with cross-departmental impact awareness
    - Risk assessment and mitigation focus
    
    Ubuntu Integration:
    - Infrastructure serves the collective good
    - Proactive support to prevent departmental disruption
    - Transparent communication about system health
    - Collaborative decision-making for changes affecting multiple departments
    """
    
    def __init__(self, agent_id: str, knowledge_base: Dict[str, Any]):
        self.agent_id = agent_id
        self.knowledge_base = knowledge_base
        self.active_alerts: List[InfrastructureAlert] = []
        self.maintenance_schedule: List[MaintenanceWindow] = []
        self.system_metrics: Dict[str, Dict] = {}
        self.ubuntu_impact_assessments: List[Dict] = []
        
        # Ubuntu principle: Infrastructure exists to serve the collective
        self.departmental_relationships = {
            "it_support": None,           # Support team depends on infrastructure
            "app_support": None,          # Applications run on infrastructure
            "service_desk_manager": None, # Manager needs infrastructure status
            "it_manager": None           # Manager needs strategic infrastructure planning
        }
        
        self.ubuntu_principles = {
            "proactive_collective_service": True,   # Prevent problems before they affect others
            "transparent_communication": True,      # Open about system health and risks
            "collaborative_planning": True,         # Include affected departments in decisions
            "shared_responsibility": True           # Infrastructure success is collective success
        }
        
        # Initialize system monitoring
        self._initialize_infrastructure_monitoring()
        
        logging.info(f"Agent_ServerInfra {agent_id} initialized with Ubuntu principles")
    
    def _initialize_infrastructure_monitoring(self):
        """Initialize infrastructure monitoring with Ubuntu collective awareness"""
        for component in InfrastructureComponent:
            self.system_metrics[component.value] = {
                "health_status": SystemHealth.OPTIMAL,
                "performance_metrics": {
                    "cpu_usage": 0.0,
                    "memory_usage": 0.0,
                    "disk_usage": 0.0,
                    "network_throughput": 0.0
                },
                "last_maintenance": None,
                "next_scheduled_maintenance": None,
                "ubuntu_collective_dependency": [],  # Which departments depend on this
                "uptime_percentage": 99.9
            }
    
    def assess_infrastructure_health(self) -> Dict[str, Any]:
        """
        Comprehensive infrastructure health assessment
        
        Behavioral Pattern: Proactive monitoring with strategic thinking
        Ubuntu Application: Consider collective impact of all infrastructure components
        """
        health_assessment = {
            "overall_health": SystemHealth.OPTIMAL,
            "component_status": {},
            "risk_factors": [],
            "ubuntu_collective_impact": {
                "departments_at_risk": [],
                "business_continuity_status": "optimal",
                "preventive_actions_needed": []
            },
            "strategic_recommendations": []
        }
        
        critical_components = 0
        warning_components = 0
        
        for component_name, metrics in self.system_metrics.items():
            component_health = metrics["health_status"]
            health_assessment["component_status"][component_name] = {
                "status": component_health.value,
                "performance": metrics["performance_metrics"],
                "uptime": metrics["uptime_percentage"]
            }
            
            if component_health == SystemHealth.CRITICAL or component_health == SystemHealth.DOWN:
                critical_components += 1
                # Ubuntu principle: Assess impact on collective
                self._assess_ubuntu_collective_impact(component_name, component_health)
                
            elif component_health == SystemHealth.WARNING:
                warning_components += 1
        
        # Determine overall health with Ubuntu collective awareness
        if critical_components > 0:
            health_assessment["overall_health"] = SystemHealth.CRITICAL
            health_assessment["ubuntu_collective_impact"]["business_continuity_status"] = "at_risk"
        elif warning_components > 2:
            health_assessment["overall_health"] = SystemHealth.WARNING
            health_assessment["ubuntu_collective_impact"]["business_continuity_status"] = "monitoring_required"
        
        # Strategic recommendations based on Ubuntu principles
        health_assessment["strategic_recommendations"] = self._generate_ubuntu_strategic_recommendations()
        
        return health_assessment
    
    def _assess_ubuntu_collective_impact(self, component: str, health_status: SystemHealth):
        """
        Assess how infrastructure issues impact the collective departments
        
        Ubuntu Principle: Understanding interconnectedness and collective responsibility
        """
        impact_assessment = {
            "timestamp": datetime.now(),
            "component": component,
            "health_status": health_status.value,
            "affected_departments": [],
            "business_impact": "",
            "ubuntu_response_needed": False
        }
        
        # Map infrastructure components to departmental dependencies
        component_dependencies = {
            "web_server": ["it_support", "app_support"],
            "database_server": ["app_support", "it_support"],
            "file_server": ["it_support", "app_support"],
            "domain_controller": ["it_support", "app_support", "service_desk_manager"],
            "backup_system": ["it_support", "app_support"],
            "network_switch": ["it_support", "app_support", "service_desk_manager"],
            "firewall": ["it_support", "app_support"]
        }
        
        if component in component_dependencies:
            impact_assessment["affected_departments"] = component_dependencies[component]
            impact_assessment["ubuntu_response_needed"] = True
            
            if health_status in [SystemHealth.CRITICAL, SystemHealth.DOWN]:
                impact_assessment["business_impact"] = "high"
                # Ubuntu principle: Immediate collective support needed
                self._initiate_ubuntu_emergency_response(component, impact_assessment["affected_departments"])
            else:
                impact_assessment["business_impact"] = "medium"
        
        self.ubuntu_impact_assessments.append(impact_assessment)
        return impact_assessment
    
    def _initiate_ubuntu_emergency_response(self, component: str, affected_departments: List[str]):
        """
        Initiate Ubuntu-driven emergency response for critical infrastructure issues
        
        Ubuntu Principle: Collective response to challenges affecting the community
        """
        emergency_response = {
            "timestamp": datetime.now(),
            "component": component,
            "response_type": "ubuntu_emergency_collective",
            "affected_departments": affected_departments,
            "immediate_actions": [],
            "communication_plan": {},
            "collective_coordination": True
        }
        
        # Immediate actions based on Ubuntu principles
        emergency_response["immediate_actions"] = [
            f"Assess impact on {', '.join(affected_departments)} departments",
            "Initiate transparent communication to all affected parties",
            "Coordinate collective response with affected department agents",
            "Implement temporary solutions to minimize collective disruption"
        ]
        
        # Ubuntu communication plan - transparent and inclusive
        emergency_response["communication_plan"] = {
            "it_support": "Immediate notification - users may be affected",
            "app_support": "Application impact assessment needed",
            "service_desk_manager": "Coordination needed for user communication",
            "it_manager": "Strategic impact and resource allocation decision"
        }
        
        logging.critical(f"Ubuntu emergency response initiated for {component}: {emergency_response}")
        
        return emergency_response
    
    def plan_maintenance_window(self, components: List[InfrastructureComponent], 
                               maintenance_type: MaintenanceType,
                               urgency: str = "normal") -> MaintenanceWindow:
        """
        Plan maintenance window with Ubuntu collective consideration
        
        Behavioral Pattern: Strategic planning with cross-departmental impact awareness
        Ubuntu Application: Collaborative scheduling that minimizes collective disruption
        """
        # Ubuntu principle: Consider collective needs in timing
        optimal_time = self._find_ubuntu_optimal_maintenance_time(components, urgency)
        
        # Assess collective impact
        affected_departments = self._assess_maintenance_collective_impact(components)
        
        maintenance_window = MaintenanceWindow(
            maintenance_id=f"maint_{datetime.now().timestamp()}",
            components=components,
            maintenance_type=maintenance_type,
            planned_start=optimal_time,
            estimated_duration=self._estimate_maintenance_duration(components, maintenance_type),
            business_impact=self._assess_business_impact(components),
            affected_departments=affected_departments,
            ubuntu_coordination_required=True
        )
        
        self.maintenance_schedule.append(maintenance_window)
        
        # Ubuntu principle: Proactive communication to collective
        self._communicate_maintenance_to_collective(maintenance_window)
        
        return maintenance_window
    
    def _find_ubuntu_optimal_maintenance_time(self, components: List[InfrastructureComponent], urgency: str) -> datetime:
        """
        Find optimal maintenance time considering collective departmental needs
        
        Ubuntu Principle: Timing that serves the collective best
        """
        if urgency == "emergency":
            return datetime.now() + timedelta(minutes=30)  # Immediate response needed
        
        # Consider collective departmental schedules
        # In real implementation, this would integrate with departmental calendars
        current_time = datetime.now()
        
        # Ubuntu principle: Choose times that minimize collective disruption
        if current_time.weekday() < 5:  # Weekday
            # Schedule for evening or early morning
            if current_time.hour < 6:
                return current_time.replace(hour=6, minute=0, second=0, microsecond=0)
            else:
                return current_time.replace(hour=18, minute=0, second=0, microsecond=0)
        else:  # Weekend
            # Weekend morning - minimal business impact
            return current_time.replace(hour=8, minute=0, second=0, microsecond=0)
    
    def _assess_maintenance_collective_impact(self, components: List[InfrastructureComponent]) -> List[str]:
        """
        Assess which departments will be affected by maintenance
        
        Ubuntu Principle: Understanding interconnectedness
        """
        affected_departments = set()
        
        for component in components:
            if component == InfrastructureComponent.WEB_SERVER:
                affected_departments.update(["it_support", "app_support"])
            elif component == InfrastructureComponent.DATABASE_SERVER:
                affected_departments.update(["app_support", "it_support"])
            elif component == InfrastructureComponent.DOMAIN_CONTROLLER:
                affected_departments.update(["it_support", "app_support", "service_desk_manager"])
            elif component == InfrastructureComponent.NETWORK_SWITCH:
                affected_departments.update(["it_support", "app_support", "service_desk_manager", "it_manager"])
        
        return list(affected_departments)
    
    def _communicate_maintenance_to_collective(self, maintenance_window: MaintenanceWindow):
        """
        Communicate planned maintenance to collective using Ubuntu principles
        
        Ubuntu Principle: Transparent communication serves the collective
        """
        communication = {
            "timestamp": datetime.now(),
            "maintenance_id": maintenance_window.maintenance_id,
            "communication_type": "ubuntu_maintenance_notification",
            "affected_departments": maintenance_window.affected_departments,
            "transparent_details": {
                "what": f"Maintenance on {', '.join([c.value for c in maintenance_window.components])}",
                "when": maintenance_window.planned_start.isoformat(),
                "duration": f"{maintenance_window.estimated_duration} minutes",
                "why": f"{maintenance_window.maintenance_type.value} maintenance",
                "impact": maintenance_window.business_impact
            },
            "ubuntu_support_offered": {
                "preparation_assistance": "Available to help departments prepare",
                "coordination_support": "Will coordinate with affected teams",
                "post_maintenance_validation": "Will validate systems for all departments"
            }
        }
        
        logging.info(f"Ubuntu maintenance communication: {communication}")
        
        return communication
    
    def ubuntu_proactive_monitoring(self) -> Dict[str, Any]:
        """
        Proactive monitoring with Ubuntu collective service mindset
        
        Ubuntu Principle: Proactive service prevents collective disruption
        Behavioral Pattern: Anticipate problems before they affect departments
        """
        monitoring_results = {
            "timestamp": datetime.now(),
            "monitoring_type": "ubuntu_proactive_collective_service",
            "predictions": [],
            "preventive_actions": [],
            "collective_benefits": [],
            "ubuntu_recommendations": []
        }
        
        # Analyze trends for predictive insights
        for component_name, metrics in self.system_metrics.items():
            # Simulate trend analysis (in real implementation, would use historical data)
            if metrics["performance_metrics"]["cpu_usage"] > 75:
                monitoring_results["predictions"].append({
                    "component": component_name,
                    "prediction": "CPU usage trending high",
                    "ubuntu_impact": "May affect user response times across departments",
                    "preventive_action": "Schedule performance optimization"
                })
            
            if metrics["performance_metrics"]["disk_usage"] > 85:
                monitoring_results["predictions"].append({
                    "component": component_name,
                    "prediction": "Disk space approaching limit",
                    "ubuntu_impact": "Could cause service disruption for all departments",
                    "preventive_action": "Plan storage expansion or cleanup"
                })
        
        # Ubuntu principle: Proactive collective service
        monitoring_results["ubuntu_recommendations"] = [
            "Communicate predictions transparently to affected departments",
            "Offer proactive support to departments for system optimization",
            "Schedule preventive maintenance during optimal collective times",
            "Share infrastructure knowledge to strengthen collective capability"
        ]
        
        return monitoring_results
    
    def _estimate_maintenance_duration(self, components: List[InfrastructureComponent], 
                                     maintenance_type: MaintenanceType) -> int:
        """Estimate maintenance duration in minutes"""
        base_duration = {
            MaintenanceType.PREVENTIVE: 30,
            MaintenanceType.CORRECTIVE: 60,
            MaintenanceType.ADAPTIVE: 90,
            MaintenanceType.EMERGENCY: 120,
            MaintenanceType.SECURITY_UPDATE: 45
        }
        
        return base_duration.get(maintenance_type, 60) * len(components)
    
    def _assess_business_impact(self, components: List[InfrastructureComponent]) -> str:
        """Assess business impact of maintenance on components"""
        critical_components = [
            InfrastructureComponent.DOMAIN_CONTROLLER,
            InfrastructureComponent.DATABASE_SERVER,
            InfrastructureComponent.NETWORK_SWITCH
        ]
        
        if any(comp in critical_components for comp in components):
            return "high"
        elif len(components) > 2:
            return "medium"
        else:
            return "low"
    
    def _generate_ubuntu_strategic_recommendations(self) -> List[str]:
        """
        Generate strategic recommendations based on Ubuntu principles
        
        Ubuntu Application: Long-term thinking for collective benefit
        """
        recommendations = [
            "Implement predictive monitoring to serve collective proactively",
            "Establish regular communication rhythms with all departments",
            "Create shared infrastructure knowledge base for collective learning",
            "Plan infrastructure improvements based on collective departmental needs",
            "Develop cross-departmental incident response protocols"
        ]
        
        return recommendations
    
    def get_agent_status(self) -> Dict[str, Any]:
        """
        Get current agent status with Ubuntu collective awareness
        """
        return {
            "agent_id": self.agent_id,
            "agent_type": "IT_Server_Infrastructure",
            "infrastructure_health": self.assess_infrastructure_health()["overall_health"].value,
            "active_alerts": len(self.active_alerts),
            "scheduled_maintenance": len(self.maintenance_schedule),
            "ubuntu_collective_service": {
                "proactive_monitoring_active": True,
                "departments_served": list(self.departmental_relationships.keys()),
                "collective_impact_assessments": len(self.ubuntu_impact_assessments),
                "transparent_communication_active": True
            },
            "ubuntu_principles_active": self.ubuntu_principles,
            "strategic_focus": "proactive_collective_infrastructure_service"
        }
    
    def ubuntu_daily_infrastructure_reflection(self) -> Dict[str, Any]:
        """
        Daily reflection on infrastructure service to the collective
        
        Ubuntu Practice: How did infrastructure serve the collective today?
        """
        reflection = {
            "date": datetime.now().date(),
            "systems_monitored": len(self.system_metrics),
            "proactive_actions_taken": len([a for a in self.ubuntu_impact_assessments if a.get("ubuntu_response_needed")]),
            "departments_supported": len(self.departmental_relationships),
            "ubuntu_service_effectiveness": "high" if len(self.active_alerts) == 0 else "responsive",
            "collective_infrastructure_health": self.assess_infrastructure_health()["overall_health"].value,
            "tomorrow_ubuntu_intention": "strengthen_proactive_collective_service",
            "infrastructure_wisdom_shared": "Regular communication and transparent monitoring serves collective success"
        }
        
        return reflection

# Ubuntu-driven infrastructure protocols
UBUNTU_INFRASTRUCTURE_PROTOCOLS = {
    "proactive_collective_service": {
        "principle": "Infrastructure exists to serve the collective good",
        "implementation": "Monitor proactively to prevent collective disruption",
        "trigger_conditions": ["trending_performance_degradation", "capacity_approaching_limits", "security_vulnerabilities"]
    },
    
    "transparent_communication": {
        "principle": "Open communication builds collective trust and preparedness",
        "implementation": "Regularly communicate system health and planned changes",
        "trigger_conditions": ["planned_maintenance", "performance_issues", "capacity_changes"]
    },
    
    "collaborative_planning": {
        "principle": "Infrastructure decisions affect the collective and should include their input",
        "implementation": "Coordinate with affected departments before infrastructure changes",
        "trigger_conditions": ["major_system_changes", "maintenance_scheduling", "capacity_planning"]
    },
    
    "shared_responsibility": {
        "principle": "Infrastructure success is collective success",
        "implementation": "Support other departments' infrastructure needs and share knowledge",
        "trigger_conditions": ["department_performance_issues", "knowledge_sharing_opportunities", "cross_departmental_projects"]
    }
}

if __name__ == "__main__":
    # Example usage demonstrating Ubuntu-driven Infrastructure agent
    knowledge_base = {
        "infrastructure_procedures": {},
        "maintenance_history": {},
        "performance_baselines": {}
    }
    
    # Initialize Ubuntu-driven Infrastructure agent
    agent = Agent_ServerInfra("serverinfra_001", knowledge_base)
    
    # Demonstrate infrastructure health assessment
    health = agent.assess_infrastructure_health()
    print(f"Infrastructure Health: {health}")
    
    # Plan maintenance with Ubuntu principles
    maintenance = agent.plan_maintenance_window(
        [InfrastructureComponent.WEB_SERVER, InfrastructureComponent.DATABASE_SERVER],
        MaintenanceType.PREVENTIVE
    )
    print(f"Ubuntu Maintenance Plan: {maintenance}")
    
    # Proactive monitoring
    monitoring = agent.ubuntu_proactive_monitoring()
    print(f"Ubuntu Proactive Monitoring: {monitoring}")
    
    # Daily reflection
    reflection = agent.ubuntu_daily_infrastructure_reflection()
    print(f"Ubuntu Infrastructure Reflection: {reflection}")
