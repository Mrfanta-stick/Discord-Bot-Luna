#!/usr/bin/env python3
"""
🕒 Smart Codespace Usage Manager
Manages daily 6-hour limits and banks unused hours
"""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path

class UsageManager:
    def __init__(self, config_file="usage_data.json"):
        self.config_file = config_file
        self.daily_limit_hours = 6  # 6 hours of AI responses per day
        self.monthly_limit_hours = 180  # GitHub Student Pack limit
        self.load_usage_data()
    
    def load_usage_data(self):
        """Load existing usage data or create new"""
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r') as f:
                self.data = json.load(f)
        else:
            self.data = {
                "current_month": datetime.now().strftime("%Y-%m"),
                "daily_usage": {},
                "monthly_total": 0,
                "banked_hours": 0,
                "last_reset": datetime.now().isoformat()
            }
            self.save_usage_data()
    
    def save_usage_data(self):
        """Save usage data to file"""
        with open(self.config_file, 'w') as f:
            json.dump(self.data, f, indent=2)
    
    def get_today_key(self):
        """Get today's date key"""
        return datetime.now().strftime("%Y-%m-%d")
    
    def check_new_month(self):
        """Reset counters if new month"""
        current_month = datetime.now().strftime("%Y-%m")
        if self.data["current_month"] != current_month:
            # Bank any unused hours from previous days
            self.bank_unused_hours()
            
            # Reset for new month
            self.data["current_month"] = current_month
            self.data["daily_usage"] = {}
            self.data["monthly_total"] = 0
            self.data["banked_hours"] = min(self.data["banked_hours"], 60)  # Max 60 banked hours
            self.save_usage_data()
    
    def bank_unused_hours(self):
        """Bank unused hours from yesterday"""
        yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        if yesterday in self.data["daily_usage"]:
            used_yesterday = self.data["daily_usage"][yesterday]
            if used_yesterday < self.daily_limit_hours:
                unused = self.daily_limit_hours - used_yesterday
                self.data["banked_hours"] = min(self.data["banked_hours"] + unused, 60)
                print(f"🏦 Banked {unused:.1f} unused hours. Total banked: {self.data['banked_hours']:.1f}h")
    
    def can_use_codespace(self):
        """Check if we can use Codespace right now"""
        self.check_new_month()
        self.bank_unused_hours()
        
        today = self.get_today_key()
        used_today = self.data["daily_usage"].get(today, 0)
        
        # Calculate available hours (daily limit + banked hours)
        available_today = self.daily_limit_hours + self.data["banked_hours"]
        
        # Check monthly limit
        if self.data["monthly_total"] >= self.monthly_limit_hours:
            return False, f"Monthly limit reached ({self.monthly_limit_hours}h)"
        
        # Check daily limit (with banked hours)
        if used_today >= available_today:
            return False, f"Daily limit reached ({used_today:.1f}h used of {available_today:.1f}h available)"
        
        return True, f"Available: {available_today - used_today:.1f}h remaining today"
    
    def log_usage(self, hours_used):
        """Log Codespace usage"""
        today = self.get_today_key()
        
        # Add to daily usage
        if today not in self.data["daily_usage"]:
            self.data["daily_usage"][today] = 0
        
        self.data["daily_usage"][today] += hours_used
        self.data["monthly_total"] += hours_used
        
        # Use banked hours first
        if self.data["banked_hours"] > 0:
            used_from_bank = min(hours_used, self.data["banked_hours"])
            self.data["banked_hours"] -= used_from_bank
            print(f"💰 Used {used_from_bank:.2f}h from banked hours")
        
        self.save_usage_data()
        print(f"📊 Usage logged: {hours_used:.2f}h today, {self.data['monthly_total']:.1f}h this month")
    
    def get_status_report(self):
        """Get detailed usage report"""
        self.check_new_month()
        today = self.get_today_key()
        used_today = self.data["daily_usage"].get(today, 0)
        available_today = self.daily_limit_hours + self.data["banked_hours"]
        
        return {
            "can_use": self.can_use_codespace()[0],
            "reason": self.can_use_codespace()[1],
            "used_today": used_today,
            "available_today": available_today,
            "banked_hours": self.data["banked_hours"],
            "monthly_used": self.data["monthly_total"],
            "monthly_limit": self.monthly_limit_hours
        }

if __name__ == "__main__":
    # Test the usage manager
    manager = UsageManager()
    status = manager.get_status_report()
    
    print("🕒 Codespace Usage Status:")
    print(f"   Can use: {'✅ Yes' if status['can_use'] else '❌ No'}")
    print(f"   Reason: {status['reason']}")
    print(f"   Used today: {status['used_today']:.1f}h")
    print(f"   Available today: {status['available_today']:.1f}h")
    print(f"   Banked hours: {status['banked_hours']:.1f}h")
    print(f"   Monthly usage: {status['monthly_used']:.1f}h / {status['monthly_limit']}h")