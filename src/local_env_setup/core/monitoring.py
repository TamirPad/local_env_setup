import logging
import time
from dataclasses import dataclass
from typing import Dict, List, Optional
from datetime import datetime

@dataclass
class SetupStep:
    name: str
    start_time: float
    end_time: Optional[float] = None
    success: Optional[bool] = None
    error: Optional[str] = None
    duration: Optional[float] = None

class SetupMonitor:
    """Monitor setup progress and track errors."""
    
    def __init__(self):
        self.steps: List[SetupStep] = []
        self.current_step: Optional[SetupStep] = None
        self.logger = logging.getLogger("SetupMonitor")
        self.start_time = time.time()
        
    def start_step(self, name: str) -> None:
        """Start tracking a setup step."""
        if self.current_step is not None:
            self.end_step(False, "Previous step not completed")
            
        self.current_step = SetupStep(
            name=name,
            start_time=time.time()
        )
        self.logger.info(f"Starting step: {name}")
        
    def end_step(self, success: bool, error: Optional[str] = None) -> None:
        """End tracking a setup step."""
        if self.current_step is None:
            return
            
        end_time = time.time()
        self.current_step.end_time = end_time
        self.current_step.success = success
        self.current_step.error = error
        self.current_step.duration = end_time - self.current_step.start_time
        
        self.steps.append(self.current_step)
        
        if success:
            self.logger.info(f"Completed step: {self.current_step.name} (duration: {self.current_step.duration:.2f}s)")
        else:
            self.logger.error(f"Failed step: {self.current_step.name} - {error}")
            
        self.current_step = None
        
    def get_summary(self) -> Dict:
        """Get a summary of the setup process."""
        total_duration = time.time() - self.start_time
        successful_steps = sum(1 for step in self.steps if step.success)
        failed_steps = sum(1 for step in self.steps if not step.success)
        
        return {
            "timestamp": datetime.now().isoformat(),
            "total_duration": total_duration,
            "total_steps": len(self.steps),
            "successful_steps": successful_steps,
            "failed_steps": failed_steps,
            "steps": [
                {
                    "name": step.name,
                    "duration": step.duration,
                    "success": step.success,
                    "error": step.error
                }
                for step in self.steps
            ]
        }
        
    def save_summary(self, filepath: str) -> None:
        """Save setup summary to a file."""
        import json
        summary = self.get_summary()
        with open(filepath, "w") as f:
            json.dump(summary, f, indent=2)
            
    def print_summary(self) -> None:
        """Print a human-readable summary of the setup process."""
        summary = self.get_summary()
        print("\nSetup Summary:")
        print(f"Total Duration: {summary['total_duration']:.2f}s")
        print(f"Total Steps: {summary['total_steps']}")
        print(f"Successful Steps: {summary['successful_steps']}")
        print(f"Failed Steps: {summary['failed_steps']}")
        
        if summary['failed_steps'] > 0:
            print("\nFailed Steps:")
            for step in summary['steps']:
                if not step['success']:
                    print(f"- {step['name']}: {step['error']}") 