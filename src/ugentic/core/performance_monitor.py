# UGENTIC Performance Monitoring Dashboard
# Real-time monitoring of Department-AI Bridge effectiveness
# Ubuntu Collaboration Metrics and System Performance Tracking

from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
import logging
from datetime import datetime, timedelta
import json
import asyncio
from collections import defaultdict, deque
import statistics

class MetricType(Enum):
    """Types of performance metrics tracked"""
    COLLABORATION_EFFECTIVENESS = "collaboration_effectiveness"
    UBUNTU_CULTURAL_INTEGRATION = "ubuntu_cultural_integration"
    USER_SATISFACTION = "user_satisfaction"
    PROCESS_IMPROVEMENT = "process_improvement"
    SYSTEM_PERFORMANCE = "system_performance"
    BRIDGE_HEALTH = "bridge_health"
    COLLECTIVE_WISDOM_EMERGENCE = "collective_wisdom_emergence"

class AlertLevel(Enum):
    """Alert severity levels"""
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"
    UBUNTU_OPPORTUNITY = "ubuntu_opportunity"  # Opportunities to deepen Ubuntu collaboration

class TrendDirection(Enum):
    """Metric trend directions"""
    IMPROVING = "improving"
    STABLE = "stable"
    DECLINING = "declining"
    FLUCTUATING = "fluctuating"

@dataclass
class PerformanceMetric:
    """Individual performance metric structure"""
    metric_id: str
    metric_type: MetricType
    metric_name: str
    current_value: float
    target_value: float
    historical_values: deque = field(default_factory=lambda: deque(maxlen=100))
    trend_direction: TrendDirection = TrendDirection.STABLE
    last_updated: datetime = field(default_factory=datetime.now)
    ubuntu_context: str = ""

@dataclass
class SystemAlert:
    """System performance alert structure"""
    alert_id: str
    alert_level: AlertLevel
    title: str
    description: str
    affected_components: List[str]
    timestamp: datetime
    ubuntu_guidance: str = ""
    suggested_actions: List[str] = field(default_factory=list)
    resolved: bool = False

@dataclass
class UbuntuCollaborationInsight:
    """Ubuntu collaboration insights and wisdom"""
    insight_id: str
    insight_type: str
    description: str
    ubuntu_principle: str
    collective_impact: str
    timestamp: datetime
    participants: List[str] = field(default_factory=list)
    wisdom_level: str = "developing"

class UGENTICPerformanceMonitor:
    """
    UGENTIC Performance Monitoring Dashboard
    
    Core Capabilities:
    - Real-time monitoring of department-AI bridge effectiveness
    - Ubuntu collaboration metrics and cultural integration tracking
    - System performance and health monitoring
    - Predictive analytics for optimization opportunities
    - Ubuntu wisdom emergence tracking
    - Alert management with Ubuntu guidance
    
    Ubuntu Integration:
    - Metrics focused on collective benefit and mutual support
    - Cultural integration depth assessment
    - Ubuntu wisdom emergence tracking
    - Collaborative decision-making effectiveness
    - Transparent performance communication
    """
    
    def __init__(self, bridge_integration_layer: Any, ubuntu_framework: Any):
        self.bridge_layer = bridge_integration_layer
        self.ubuntu_framework = ubuntu_framework
        
        # Performance metrics storage
        self.metrics: Dict[str, PerformanceMetric] = {}
        self.alerts: List[SystemAlert] = []
        self.ubuntu_insights: List[UbuntuCollaborationInsight] = []
        
        # Monitoring configuration
        self.monitoring_active = False
        self.monitoring_interval = 30  # seconds
        self.metric_history_window = timedelta(hours=24)
        
        # Ubuntu monitoring principles
        self.ubuntu_monitoring_principles = {
            "transparent_performance_communication": True,
            "collective_benefit_measurement": True,
            "cultural_sensitivity_tracking": True,
            "wisdom_emergence_recognition": True,
            "collaborative_improvement_focus": True
        }
        
        # Initialize monitoring systems
        self._initialize_performance_metrics()
        self._initialize_ubuntu_tracking()
        
        logging.info("UGENTIC Performance Monitor initialized with Ubuntu-focused metrics")
    
    def _initialize_performance_metrics(self):
        """Initialize core performance metrics"""
        
        # Bridge Integration Metrics
        self.metrics["bridge_connection_health"] = PerformanceMetric(
            metric_id="bridge_connection_health",
            metric_type=MetricType.BRIDGE_HEALTH,
            metric_name="Bridge Connection Health",
            current_value=0.0,
            target_value=0.95,
            ubuntu_context="Healthy bridges enable Ubuntu collaboration between AI and humans"
        )
        
        self.metrics["collaboration_effectiveness"] = PerformanceMetric(
            metric_id="collaboration_effectiveness",
            metric_type=MetricType.COLLABORATION_EFFECTIVENESS,
            metric_name="AI-Human Collaboration Effectiveness",
            current_value=0.0,
            target_value=0.85,
            ubuntu_context="Effective collaboration reflects Ubuntu principle of mutual support"
        )
        
        # Ubuntu Cultural Integration Metrics
        self.metrics["ubuntu_cultural_depth"] = PerformanceMetric(
            metric_id="ubuntu_cultural_depth",
            metric_type=MetricType.UBUNTU_CULTURAL_INTEGRATION,
            metric_name="Ubuntu Cultural Integration Depth",
            current_value=0.0,
            target_value=0.80,
            ubuntu_context="Deep cultural integration honors Ubuntu authenticity and wisdom"
        )
        
        self.metrics["collective_wisdom_emergence"] = PerformanceMetric(
            metric_id="collective_wisdom_emergence",
            metric_type=MetricType.COLLECTIVE_WISDOM_EMERGENCE,
            metric_name="Collective Wisdom Emergence",
            current_value=0.0,
            target_value=0.75,
            ubuntu_context="Collective wisdom emerges when Ubuntu principles guide collaboration"
        )
        
        # User Experience Metrics
        self.metrics["user_satisfaction"] = PerformanceMetric(
            metric_id="user_satisfaction",
            metric_type=MetricType.USER_SATISFACTION,
            metric_name="User Satisfaction with AI Integration",
            current_value=0.0,
            target_value=0.90,
            ubuntu_context="User satisfaction reflects AI serving collective empowerment"
        )
        
        self.metrics["process_improvement"] = PerformanceMetric(
            metric_id="process_improvement",
            metric_name="Process Improvement Impact",
            metric_type=MetricType.PROCESS_IMPROVEMENT,
            current_value=0.0,
            target_value=0.70,
            ubuntu_context="Process improvements serve collective efficiency and effectiveness"
        )
        
        # System Performance Metrics
        self.metrics["system_responsiveness"] = PerformanceMetric(
            metric_id="system_responsiveness",
            metric_type=MetricType.SYSTEM_PERFORMANCE,
            metric_name="System Response Time",
            current_value=0.0,
            target_value=0.95,
            ubuntu_context="Responsive systems support seamless Ubuntu collaboration"
        )
    
    def _initialize_ubuntu_tracking(self):
        """Initialize Ubuntu-specific tracking capabilities"""
        
        # Ubuntu collaboration patterns to track
        self.ubuntu_patterns = {
            "mutual_support_instances": 0,
            "collective_decision_making": 0,
            "knowledge_sharing_events": 0,
            "consensus_building_sessions": 0,
            "ubuntu_wisdom_applications": 0,
            "cultural_deepening_moments": 0
        }
        
        # Ubuntu wisdom emergence indicators
        self.ubuntu_wisdom_indicators = [
            "transcendent_collective_insights",
            "spontaneous_mutual_support",
            "authentic_cultural_expression",
            "collective_problem_solving_excellence",
            "ubuntu_relationship_deepening"
        ]
    
    async def start_monitoring(self):
        """Start continuous performance monitoring"""
        
        if self.monitoring_active:
            logging.warning("Monitoring already active")
            return
        
        self.monitoring_active = True
        logging.info("Starting UGENTIC performance monitoring")
        
        # Start monitoring tasks
        monitoring_tasks = [
            asyncio.create_task(self._monitor_bridge_performance()),
            asyncio.create_task(self._monitor_ubuntu_collaboration()),
            asyncio.create_task(self._monitor_system_health()),
            asyncio.create_task(self._analyze_trends_and_alerts()),
            asyncio.create_task(self._track_ubuntu_wisdom_emergence())
        ]
        
        try:
            await asyncio.gather(*monitoring_tasks)
        except Exception as e:
            logging.error(f"Monitoring error: {e}")
            self.monitoring_active = False
    
    async def _monitor_bridge_performance(self):
        """Monitor department-AI bridge performance"""
        
        while self.monitoring_active:
            try:
                # Get bridge status from integration layer
                if hasattr(self.bridge_layer, 'get_bridge_status_report'):
                    bridge_report = await self.bridge_layer.get_bridge_status_report()
                    
                    # Update bridge health metrics
                    total_bridges = bridge_report.get('total_active_bridges', 0)
                    if total_bridges > 0:
                        # Calculate bridge health based on active connections and status
                        healthy_bridges = sum(1 for bridge in bridge_report.get('bridge_connections', {}).values()
                                            if bridge.get('status') in ['connected', 'active_collaboration', 'ubuntu_harmony'])
                        
                        bridge_health = healthy_bridges / total_bridges
                        await self._update_metric('bridge_connection_health', bridge_health)
                        
                        # Update collaboration effectiveness
                        avg_ubuntu_level = bridge_report.get('ubuntu_collaboration_summary', {}).get('average_ubuntu_collaboration_level', 0)
                        await self._update_metric('collaboration_effectiveness', avg_ubuntu_level)
                        
                        # Update Ubuntu cultural integration
                        integration_metrics = bridge_report.get('integration_effectiveness', {})
                        ubuntu_cultural = integration_metrics.get('ubuntu_cultural_integration', 0)
                        await self._update_metric('ubuntu_cultural_depth', ubuntu_cultural)
                        
                        # Update user satisfaction
                        user_satisfaction = integration_metrics.get('user_satisfaction', 0)
                        await self._update_metric('user_satisfaction', user_satisfaction)
                        
                        # Update process improvement
                        process_improvement = integration_metrics.get('process_improvement', 0)
                        await self._update_metric('process_improvement', process_improvement)
                
                else:
                    # Simulate metrics for development
                    await self._simulate_bridge_metrics()
                
            except Exception as e:
                logging.error(f"Bridge performance monitoring error: {e}")
            
            await asyncio.sleep(self.monitoring_interval)
    
    async def _monitor_ubuntu_collaboration(self):
        """Monitor Ubuntu collaboration patterns and effectiveness"""
        
        while self.monitoring_active:
            try:
                # Track Ubuntu collaboration patterns
                if hasattr(self.ubuntu_framework, 'get_framework_status'):
                    framework_status = self.ubuntu_framework.get_framework_status()
                    
                    # Update collective wisdom emergence based on active collaborations
                    active_collaborations = framework_status.get('active_collaborations', 0)
                    framework_effectiveness = framework_status.get('framework_effectiveness', {})
                    
                    if framework_effectiveness:
                        wisdom_emergence = 0.7 if active_collaborations > 0 else 0.3
                        await self._update_metric('collective_wisdom_emergence', wisdom_emergence)
                
                # Track Ubuntu patterns
                await self._track_ubuntu_patterns()
                
                # Generate Ubuntu insights
                await self._generate_ubuntu_insights()
                
            except Exception as e:
                logging.error(f"Ubuntu collaboration monitoring error: {e}")
            
            await asyncio.sleep(self.monitoring_interval)
    
    async def _monitor_system_health(self):
        """Monitor overall system performance and health"""
        
        while self.monitoring_active:
            try:
                # Simulate system performance metrics
                import time
                start_time = time.time()
                
                # Simulate system operation
                await asyncio.sleep(0.1)
                
                response_time = time.time() - start_time
                responsiveness = max(0, 1.0 - (response_time - 0.1) / 0.9)  # Scale to 0-1
                
                await self._update_metric('system_responsiveness', responsiveness)
                
            except Exception as e:
                logging.error(f"System health monitoring error: {e}")
            
            await asyncio.sleep(self.monitoring_interval)
    
    async def _track_ubuntu_patterns(self):
        """Track Ubuntu collaboration patterns and cultural integration"""
        
        # Simulate Ubuntu pattern tracking (in production, would track real events)
        import random
        
        # Randomly increment Ubuntu patterns to simulate real activity
        if random.random() > 0.7:  # 30% chance of Ubuntu activity
            pattern = random.choice(list(self.ubuntu_patterns.keys()))
            self.ubuntu_patterns[pattern] += 1
            
            # Generate Ubuntu insight for significant patterns
            if self.ubuntu_patterns[pattern] % 5 == 0:  # Every 5th occurrence
                await self._create_ubuntu_insight(pattern)
    
    async def _create_ubuntu_insight(self, pattern_type: str):
        """Create Ubuntu collaboration insight"""
        
        ubuntu_insights = {
            "mutual_support_instances": {
                "description": "Increased mutual support between AI agents and department staff",
                "ubuntu_principle": "I am because we are - mutual support strengthens collective capability",
                "collective_impact": "Enhanced team collaboration and problem-solving effectiveness"
            },
            "collective_decision_making": {
                "description": "Collaborative decision-making between AI and human expertise",
                "ubuntu_principle": "Collective wisdom emerges through authentic dialogue and shared responsibility",
                "collective_impact": "Improved decision quality through diverse perspectives and shared accountability"
            },
            "knowledge_sharing_events": {
                "description": "Active knowledge sharing between AI agents and department experts",
                "ubuntu_principle": "Knowledge belongs to the collective and strengthens everyone",
                "collective_impact": "Enhanced collective learning and capability development"
            }
        }
        
        insight_data = ubuntu_insights.get(pattern_type, {
            "description": f"Ubuntu pattern observed: {pattern_type}",
            "ubuntu_principle": "Ubuntu principles guide collaborative excellence",
            "collective_impact": "Positive impact on collective capability"
        })
        
        insight = UbuntuCollaborationInsight(
            insight_id=f"ubuntu_insight_{datetime.now().timestamp()}",
            insight_type=pattern_type,
            description=insight_data["description"],
            ubuntu_principle=insight_data["ubuntu_principle"],
            collective_impact=insight_data["collective_impact"],
            timestamp=datetime.now(),
            participants=["AI_agents", "department_staff"],
            wisdom_level="developing"
        )
        
        self.ubuntu_insights.append(insight)
        
        # Keep only recent insights
        cutoff_time = datetime.now() - timedelta(days=7)
        self.ubuntu_insights = [i for i in self.ubuntu_insights if i.timestamp > cutoff_time]
    
    async def _analyze_trends_and_alerts(self):
        """Analyze metric trends and generate alerts"""
        
        while self.monitoring_active:
            try:
                current_time = datetime.now()
                
                for metric_id, metric in self.metrics.items():
                    # Update trend direction
                    if len(metric.historical_values) >= 3:
                        recent_values = list(metric.historical_values)[-3:]
                        trend = self._calculate_trend(recent_values)
                        metric.trend_direction = trend
                    
                    # Check for alerts
                    await self._check_metric_alerts(metric)
                
                # Clean up old alerts
                self._cleanup_old_alerts()
                
            except Exception as e:
                logging.error(f"Trend analysis error: {e}")
            
            await asyncio.sleep(self.monitoring_interval * 2)  # Less frequent analysis
    
    async def _track_ubuntu_wisdom_emergence(self):
        """Track emergence of Ubuntu wisdom and cultural deepening"""
        
        while self.monitoring_active:
            try:
                # Look for Ubuntu wisdom emergence indicators
                current_ubuntu_level = self.metrics.get('ubuntu_cultural_depth', PerformanceMetric('', MetricType.UBUNTU_CULTURAL_INTEGRATION, '', 0, 0)).current_value
                collaboration_effectiveness = self.metrics.get('collaboration_effectiveness', PerformanceMetric('', MetricType.COLLABORATION_EFFECTIVENESS, '', 0, 0)).current_value
                
                # Detect wisdom emergence
                if current_ubuntu_level > 0.75 and collaboration_effectiveness > 0.8:
                    wisdom_emergence_level = min(1.0, (current_ubuntu_level + collaboration_effectiveness) / 2)
                    await self._update_metric('collective_wisdom_emergence', wisdom_emergence_level)
                    
                    # Generate Ubuntu opportunity alert
                    if wisdom_emergence_level > 0.85:
                        await self._create_ubuntu_opportunity_alert(wisdom_emergence_level)
                
            except Exception as e:
                logging.error(f"Ubuntu wisdom tracking error: {e}")
            
            await asyncio.sleep(self.monitoring_interval * 3)  # Even less frequent wisdom tracking
    
    async def _update_metric(self, metric_id: str, value: float):
        """Update metric value and historical data"""
        
        if metric_id not in self.metrics:
            logging.warning(f"Unknown metric: {metric_id}")
            return
        
        metric = self.metrics[metric_id]
        metric.current_value = value
        metric.historical_values.append(value)
        metric.last_updated = datetime.now()
    
    def _calculate_trend(self, values: List[float]) -> TrendDirection:
        """Calculate trend direction from recent values"""
        
        if len(values) < 2:
            return TrendDirection.STABLE
        
        # Simple trend calculation
        if values[-1] > values[-2] * 1.05:  # 5% improvement
            return TrendDirection.IMPROVING
        elif values[-1] < values[-2] * 0.95:  # 5% decline
            return TrendDirection.DECLINING
        else:
            return TrendDirection.STABLE
    
    async def _check_metric_alerts(self, metric: PerformanceMetric):
        """Check metric for alert conditions"""
        
        # Critical alert if significantly below target
        if metric.current_value < metric.target_value * 0.7:
            await self._create_alert(
                AlertLevel.CRITICAL,
                f"Critical: {metric.metric_name} Below Target",
                f"{metric.metric_name} is at {metric.current_value:.2f}, significantly below target of {metric.target_value:.2f}",
                [metric.metric_id],
                metric.ubuntu_context
            )
        
        # Warning alert if below target
        elif metric.current_value < metric.target_value * 0.85:
            await self._create_alert(
                AlertLevel.WARNING,
                f"Warning: {metric.metric_name} Below Target",
                f"{metric.metric_name} is at {metric.current_value:.2f}, below target of {metric.target_value:.2f}",
                [metric.metric_id],
                metric.ubuntu_context
            )
        
        # Declining trend alert
        elif metric.trend_direction == TrendDirection.DECLINING:
            await self._create_alert(
                AlertLevel.WARNING,
                f"Declining Trend: {metric.metric_name}",
                f"{metric.metric_name} showing declining trend",
                [metric.metric_id],
                f"Ubuntu guidance: {metric.ubuntu_context}"
            )
    
    async def _create_alert(self, level: AlertLevel, title: str, description: str, 
                          affected_components: List[str], ubuntu_guidance: str = ""):
        """Create system alert with Ubuntu guidance"""
        
        # Check if similar alert already exists
        existing_alert = next((a for a in self.alerts 
                             if a.title == title and not a.resolved), None)
        
        if existing_alert:
            return  # Don't create duplicate alerts
        
        alert = SystemAlert(
            alert_id=f"alert_{datetime.now().timestamp()}",
            alert_level=level,
            title=title,
            description=description,
            affected_components=affected_components,
            timestamp=datetime.now(),
            ubuntu_guidance=ubuntu_guidance,
            suggested_actions=self._generate_ubuntu_guided_actions(level, affected_components)
        )
        
        self.alerts.append(alert)
        logging.info(f"Alert created: {alert.title} ({alert.alert_level.value})")
    
    async def _create_ubuntu_opportunity_alert(self, wisdom_level: float):
        """Create Ubuntu opportunity alert for cultural deepening"""
        
        await self._create_alert(
            AlertLevel.UBUNTU_OPPORTUNITY,
            "Ubuntu Wisdom Emergence Opportunity",
            f"High Ubuntu collaboration level ({wisdom_level:.2f}) indicates opportunity for cultural deepening",
            ["ubuntu_cultural_integration"],
            "This is an excellent opportunity to deepen Ubuntu cultural integration and collective wisdom emergence"
        )
    
    def _generate_ubuntu_guided_actions(self, level: AlertLevel, components: List[str]) -> List[str]:
        """Generate Ubuntu-guided suggested actions for alerts"""
        
        actions = []
        
        if level == AlertLevel.CRITICAL:
            actions.extend([
                "Convene Ubuntu-guided collective problem-solving session",
                "Assess how mutual support can address the critical issue",
                "Engage all affected stakeholders in transparent dialogue"
            ])
        
        elif level == AlertLevel.WARNING:
            actions.extend([
                "Apply Ubuntu principle of proactive mutual support",
                "Share knowledge and resources to strengthen affected area",
                "Foster collaborative approach to improvement"
            ])
        
        elif level == AlertLevel.UBUNTU_OPPORTUNITY:
            actions.extend([
                "Organize Ubuntu cultural deepening session",
                "Document and share Ubuntu wisdom insights",
                "Plan expansion of Ubuntu collaboration practices"
            ])
        
        # Component-specific actions
        if "ubuntu_cultural_integration" in components:
            actions.append("Focus on authentic Ubuntu cultural practices and relationship building")
        
        if "collaboration_effectiveness" in components:
            actions.append("Strengthen mutual support and collective decision-making processes")
        
        return actions
    
    def _cleanup_old_alerts(self):
        """Clean up resolved and old alerts"""
        
        # Remove alerts older than 7 days or resolved alerts older than 1 day
        cutoff_time = datetime.now() - timedelta(days=7)
        resolved_cutoff = datetime.now() - timedelta(days=1)
        
        self.alerts = [a for a in self.alerts 
                      if (a.timestamp > cutoff_time and not a.resolved) or 
                         (a.resolved and a.timestamp > resolved_cutoff)]
    
    async def _simulate_bridge_metrics(self):
        """Simulate bridge metrics for development mode"""
        
        import random
        
        # Simulate improving metrics over time
        base_improvement = 0.01
        
        metrics_to_simulate = [
            'bridge_connection_health', 'collaboration_effectiveness',
            'ubuntu_cultural_depth', 'user_satisfaction', 'process_improvement'
        ]
        
        for metric_id in metrics_to_simulate:
            if metric_id in self.metrics:
                current = self.metrics[metric_id].current_value
                # Add small random improvement with occasional variance
                change = random.uniform(-0.02, 0.05)  # Slightly positive bias
                new_value = max(0, min(1.0, current + change))
                await self._update_metric(metric_id, new_value)
    
    async def get_performance_dashboard(self) -> Dict[str, Any]:
        """Get comprehensive performance dashboard data"""
        
        dashboard_data = {
            "dashboard_timestamp": datetime.now().isoformat(),
            "monitoring_status": "active" if self.monitoring_active else "inactive",
            "metrics_summary": {},
            "alerts_summary": {},
            "ubuntu_collaboration_insights": {},
            "trend_analysis": {},
            "ubuntu_wisdom_emergence": {},
            "recommendations": []
        }
        
        # Metrics summary
        for metric_id, metric in self.metrics.items():
            dashboard_data["metrics_summary"][metric_id] = {
                "name": metric.metric_name,
                "current_value": metric.current_value,
                "target_value": metric.target_value,
                "trend": metric.trend_direction.value,
                "last_updated": metric.last_updated.isoformat(),
                "ubuntu_context": metric.ubuntu_context,
                "performance_vs_target": metric.current_value / metric.target_value if metric.target_value > 0 else 0
            }
        
        # Alerts summary
        active_alerts = [a for a in self.alerts if not a.resolved]
        dashboard_data["alerts_summary"] = {
            "total_active_alerts": len(active_alerts),
            "critical_alerts": len([a for a in active_alerts if a.alert_level == AlertLevel.CRITICAL]),
            "warning_alerts": len([a for a in active_alerts if a.alert_level == AlertLevel.WARNING]),
            "ubuntu_opportunities": len([a for a in active_alerts if a.alert_level == AlertLevel.UBUNTU_OPPORTUNITY]),
            "recent_alerts": [
                {
                    "title": a.title,
                    "level": a.alert_level.value,
                    "timestamp": a.timestamp.isoformat(),
                    "ubuntu_guidance": a.ubuntu_guidance
                } for a in sorted(active_alerts, key=lambda x: x.timestamp, reverse=True)[:5]
            ]
        }
        
        # Ubuntu collaboration insights
        recent_insights = [i for i in self.ubuntu_insights if i.timestamp > datetime.now() - timedelta(days=1)]
        dashboard_data["ubuntu_collaboration_insights"] = {
            "total_insights": len(self.ubuntu_insights),
            "recent_insights": len(recent_insights),
            "ubuntu_patterns": self.ubuntu_patterns.copy(),
            "latest_insights": [
                {
                    "type": i.insight_type,
                    "description": i.description,
                    "ubuntu_principle": i.ubuntu_principle,
                    "timestamp": i.timestamp.isoformat()
                } for i in sorted(recent_insights, key=lambda x: x.timestamp, reverse=True)[:3]
            ]
        }
        
        # Ubuntu wisdom emergence
        wisdom_metric = self.metrics.get('collective_wisdom_emergence')
        if wisdom_metric:
            dashboard_data["ubuntu_wisdom_emergence"] = {
                "current_level": wisdom_metric.current_value,
                "wisdom_indicators": self.ubuntu_wisdom_indicators,
                "emergence_trend": wisdom_metric.trend_direction.value,
                "cultural_depth": self.metrics.get('ubuntu_cultural_depth', type('', (), {'current_value': 0})).current_value
            }
        
        # Generate recommendations
        dashboard_data["recommendations"] = self._generate_dashboard_recommendations()
        
        return dashboard_data
    
    def _generate_dashboard_recommendations(self) -> List[str]:
        """Generate Ubuntu-guided recommendations based on current performance"""
        
        recommendations = []
        
        # Check overall performance
        avg_performance = statistics.mean([m.current_value / m.target_value for m in self.metrics.values() if m.target_value > 0])
        
        if avg_performance >= 0.9:
            recommendations.append("Excellent performance! Focus on Ubuntu cultural deepening and wisdom sharing")
        elif avg_performance >= 0.8:
            recommendations.append("Strong performance. Consider expanding Ubuntu collaboration practices")
        elif avg_performance >= 0.7:
            recommendations.append("Good foundation. Apply Ubuntu mutual support to strengthen weaker areas")
        else:
            recommendations.append("Performance needs attention. Convene Ubuntu collective problem-solving session")
        
        # Specific Ubuntu recommendations
        ubuntu_cultural = self.metrics.get('ubuntu_cultural_depth', type('', (), {'current_value': 0})).current_value
        if ubuntu_cultural > 0.8:
            recommendations.append("Ubuntu cultural integration is strong - share insights with broader organization")
        elif ubuntu_cultural < 0.6:
            recommendations.append("Focus on authentic Ubuntu cultural practices and relationship building")
        
        # Alert-based recommendations
        critical_alerts = [a for a in self.alerts if a.alert_level == AlertLevel.CRITICAL and not a.resolved]
        if critical_alerts:
            recommendations.append("Address critical alerts through Ubuntu collaborative problem-solving")
        
        return recommendations
    
    async def stop_monitoring(self):
        """Stop performance monitoring"""
        
        self.monitoring_active = False
        logging.info("UGENTIC performance monitoring stopped")

# Example usage and testing
if __name__ == "__main__":
    async def test_performance_monitoring():
        """Test UGENTIC Performance Monitoring Dashboard"""
        
        print(" UGENTIC Performance Monitoring Dashboard Test")
        print("=" * 55)
        
        # Mock dependencies
        bridge_layer = type('MockBridge', (), {
            'get_bridge_status_report': lambda: {
                'total_active_bridges': 3,
                'ubuntu_collaboration_summary': {'average_ubuntu_collaboration_level': 0.75},
                'integration_effectiveness': {
                    'ubuntu_cultural_integration': 0.7,
                    'user_satisfaction': 0.85,
                    'process_improvement': 0.6
                }
            }
        })()
        
        ubuntu_framework = type('MockUbuntu', (), {
            'get_framework_status': lambda: {
                'active_collaborations': 2,
                'framework_effectiveness': {'collaboration_facilitation': 'high'}
            }
        })()
        
        # Initialize performance monitor
        monitor = UGENTICPerformanceMonitor(bridge_layer, ubuntu_framework)
        
        # Test dashboard generation
        print("Getting performance dashboard...")
        dashboard = await monitor.get_performance_dashboard()
        
        print(f"Monitoring Status: {dashboard['monitoring_status']}")
        print(f"Total Metrics: {len(dashboard['metrics_summary'])}")
        print(f"Active Alerts: {dashboard['alerts_summary']['total_active_alerts']}")
        print(f"Ubuntu Insights: {dashboard['ubuntu_collaboration_insights']['total_insights']}")
        
        # Display key metrics
        print("\nKey Metrics:")
        for metric_id, metric_data in dashboard["metrics_summary"].items():
            print(f"• {metric_data['name']}: {metric_data['current_value']:.2f} (Target: {metric_data['target_value']:.2f})")
        
        print("\nUbuntu Patterns:")
        for pattern, count in dashboard["ubuntu_collaboration_insights"]["ubuntu_patterns"].items():
            print(f"• {pattern.replace('_', ' ').title()}: {count}")
        
        print("\nRecommendations:")
        for rec in dashboard["recommendations"]:
            print(f"• {rec}")
        
        print("\n Performance monitoring test completed successfully!")
    
    # Run test
    asyncio.run(test_performance_monitoring())
