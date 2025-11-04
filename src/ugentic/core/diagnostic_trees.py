"""
Diagnostic Trees - Standard IT Support Procedures (SESSION 30)
Provides structured diagnostic procedures for common IT issues
Reduces LLM iteration count by providing proven troubleshooting sequences
"""

from typing import Dict, List, Any
from dataclasses import dataclass


@dataclass
class DiagnosticStep:
    """A single step in a diagnostic procedure"""
    step_number: int
    action: str
    tool: str
    rationale: str
    next_if_success: str  # What to do if this step succeeds
    next_if_fail: str     # What to do if this step fails


class DiagnosticTrees:
    """
    Standard diagnostic procedures for common IT support issues
    
    SESSION 30 OPTIMIZATION:
    - Provides proven troubleshooting sequences
    - Reduces LLM guesswork and iteration count
    - Based on real-world IT support procedures
    
    Philosophy:
    - Agent-guided (provide structure)
    - LLM-enhanced (agent can deviate if justified)
    - Experience-based (mirrors real technician knowledge)
    """
    
    def __init__(self):
        """Initialize diagnostic trees for common scenarios"""
        
        # Printer troubleshooting tree
        self.printer_tree = [
            DiagnosticStep(
                step_number=1,
                action="Check if printer is online and responding",
                tool="check_printer_status",
                rationale="First verify basic printer connectivity and status",
                next_if_success="Go to step 2",
                next_if_fail="Printer is offline - check physical connectivity, power, network cable/WiFi"
            ),
            DiagnosticStep(
                step_number=2,
                action="Check if user has permissions to use the printer",
                tool="check_user_permissions",
                rationale="Most common cause of 'can't print' when printer is online",
                next_if_success="Go to step 3",
                next_if_fail="Permission denied - grant user access to printer or relevant print group"
            ),
            DiagnosticStep(
                step_number=3,
                action="Verify print spooler/driver software is installed",
                tool="check_software_installation",
                rationale="Ensure user has required print drivers",
                next_if_success="Issue resolved - all components working",
                next_if_fail="Install/reinstall printer driver software"
            )
        ]
        
        # Account lockout tree
        self.account_lockout_tree = [
            DiagnosticStep(
                step_number=1,
                action="Get user profile and account status",
                tool="get_user_profile",
                rationale="Verify account is locked and get lockout details",
                next_if_success="Go to step 2",
                next_if_fail="Account not found or other profile issue"
            ),
            DiagnosticStep(
                step_number=2,
                action="Check recent ticket history for recurring locks",
                tool="get_recent_tickets",
                rationale="Determine if this is recurring (may indicate compromised credentials)",
                next_if_success="Go to step 3",
                next_if_fail="No history available, proceed to unlock"
            ),
            DiagnosticStep(
                step_number=3,
                action="Unlock the account",
                tool="unlock_user_account",
                rationale="Standard remediation for account lockout",
                next_if_success="Account unlocked - advise user to update saved credentials",
                next_if_fail="Unlock failed - may require password reset or admin intervention"
            )
        ]
        
        # Password reset tree
        self.password_reset_tree = [
            DiagnosticStep(
                step_number=1,
                action="Get user profile to verify identity and account status",
                tool="get_user_profile",
                rationale="Verify user identity and check for account issues",
                next_if_success="Go to step 2",
                next_if_fail="Account not found or identity verification failed"
            ),
            DiagnosticStep(
                step_number=2,
                action="Reset user password",
                tool="reset_user_password",
                rationale="Standard password reset procedure",
                next_if_success="Password reset complete - provide temp password securely",
                next_if_fail="Reset failed - may require admin escalation"
            )
        ]
        
        # Email configuration tree
        self.email_config_tree = [
            DiagnosticStep(
                step_number=1,
                action="Verify email configuration settings",
                tool="verify_email_config",
                rationale="Check if email client is configured correctly",
                next_if_success="Configuration correct - go to step 2",
                next_if_fail="Configuration issue - fix server settings, ports, authentication"
            ),
            DiagnosticStep(
                step_number=2,
                action="Check user permissions for email access",
                tool="check_user_permissions",
                rationale="Verify user has mailbox access permissions",
                next_if_success="Permissions correct - check network/remote access",
                next_if_fail="Permission denied - grant mailbox access or distribution list membership"
            ),
            DiagnosticStep(
                step_number=3,
                action="Test remote access if applicable",
                tool="test_remote_access",
                rationale="VPN or remote connectivity may be affecting email",
                next_if_success="Remote access working - issue resolved",
                next_if_fail="VPN/remote access issue - check connectivity"
            )
        ]
        
        # Remote access tree
        self.remote_access_tree = [
            DiagnosticStep(
                step_number=1,
                action="Test remote access/VPN connectivity",
                tool="test_remote_access",
                rationale="First verify if VPN is connecting",
                next_if_success="VPN connects - go to step 2",
                next_if_fail="VPN not connecting - check credentials, network, VPN service status"
            ),
            DiagnosticStep(
                step_number=2,
                action="Check user permissions for remote access",
                tool="check_user_permissions",
                rationale="Verify user has VPN/remote access permissions",
                next_if_success="Has permissions - issue may be client-side or network",
                next_if_fail="No VPN permissions - request access or add to VPN group"
            ),
            DiagnosticStep(
                step_number=3,
                action="Verify software installation (VPN client)",
                tool="check_software_installation",
                rationale="Ensure VPN client software is properly installed",
                next_if_success="Client installed correctly - issue resolved",
                next_if_fail="VPN client missing/corrupted - reinstall VPN software"
            )
        ]
    
    def get_diagnostic_tree(self, problem_type: str) -> List[DiagnosticStep]:
        """
        Get diagnostic tree for a specific problem type
        
        Args:
            problem_type: Type of problem (printer, account_lockout, password_reset, etc.)
            
        Returns:
            List of diagnostic steps, or empty list if no tree available
        """
        trees = {
            'printer': self.printer_tree,
            'account_lockout': self.account_lockout_tree,
            'account_locked': self.account_lockout_tree,
            'locked_out': self.account_lockout_tree,
            'password_reset': self.password_reset_tree,
            'password': self.password_reset_tree,
            'forgot_password': self.password_reset_tree,
            'email': self.email_config_tree,
            'email_config': self.email_config_tree,
            'outlook': self.email_config_tree,
            'remote_access': self.remote_access_tree,
            'vpn': self.remote_access_tree,
            'remote': self.remote_access_tree
        }
        
        return trees.get(problem_type.lower(), [])
    
    def identify_problem_type(self, problem_description: str) -> str:
        """
        Identify problem type from description using keyword matching
        
        Args:
            problem_description: User's problem description
            
        Returns:
            Problem type string, or "unknown" if can't determine
        """
        problem_lower = problem_description.lower()
        
        # Keyword patterns for each problem type
        patterns = {
            'printer': ['print', 'printer', 'printing', 'cant print', "can't print"],
            'account_lockout': ['locked', 'lock out', 'lockout', 'account locked', 'cant login', "can't login", "can't log in"],
            'password_reset': ['password', 'forgot password', 'reset password', 'cant remember password'],
            'email': ['email', 'outlook', 'mail', 'mailbox', 'cant send email', 'cant receive email'],
            'remote_access': ['vpn', 'remote access', 'remote desktop', 'work from home', 'rdp', 'remote']
        }
        
        # Check each pattern
        for problem_type, keywords in patterns.items():
            for keyword in keywords:
                if keyword in problem_lower:
                    return problem_type
        
        return "unknown"
    
    def format_tree_for_prompt(self, steps: List[DiagnosticStep]) -> str:
        """
        Format diagnostic tree as a structured prompt for the LLM
        
        Args:
            steps: List of diagnostic steps
            
        Returns:
            Formatted string for inclusion in agent prompt
        """
        if not steps:
            return ""
        
        prompt = "\n**STANDARD DIAGNOSTIC PROCEDURE:**\n"
        prompt += "Follow these proven steps (you may deviate if situation warrants):\n\n"
        
        for step in steps:
            prompt += f"**Step {step.step_number}:** {step.action}\n"
            prompt += f"  - Tool: `{step.tool}`\n"
            prompt += f"  - Rationale: {step.rationale}\n"
            prompt += f"  - If successful: {step.next_if_success}\n"
            prompt += f"  - If fails: {step.next_if_fail}\n\n"
        
        return prompt
    
    def get_available_trees(self) -> List[str]:
        """Get list of available diagnostic tree types"""
        return [
            'printer',
            'account_lockout',
            'password_reset',
            'email',
            'remote_access'
        ]
    
    def get_tree_summary(self) -> Dict[str, Any]:
        """Get summary of all available diagnostic trees"""
        return {
            'total_trees': len(self.get_available_trees()),
            'trees': {
                'printer': f"{len(self.printer_tree)} steps",
                'account_lockout': f"{len(self.account_lockout_tree)} steps",
                'password_reset': f"{len(self.password_reset_tree)} steps",
                'email': f"{len(self.email_config_tree)} steps",
                'remote_access': f"{len(self.remote_access_tree)} steps"
            },
            'purpose': 'Reduce LLM iteration count by providing structured procedures',
            'optimization': 'SESSION 30'
        }
