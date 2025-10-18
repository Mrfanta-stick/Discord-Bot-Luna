#!/usr/bin/env python3
"""
🛠️ Usage Admin Tool
Manage Luna's Codespace usage limits and banking
"""

import argparse
from usage_manager import UsageManager

def main():
    parser = argparse.ArgumentParser(description="Manage Luna's Codespace usage")
    parser.add_argument('--status', action='store_true', help='Show current status')
    parser.add_argument('--bank', type=float, help='Manually bank hours (up to 60h total)')
    parser.add_argument('--reset-day', action='store_true', help='Reset today\'s usage')
    parser.add_argument('--reset-month', action='store_true', help='Reset monthly usage')
    
    args = parser.parse_args()
    manager = UsageManager()
    
    if args.status or not any(vars(args).values()):
        # Show status (default action)
        status = manager.get_status_report()
        print("🕒 Codespace Usage Status:")
        print(f"   Can use: {'✅ Yes' if status['can_use'] else '❌ No'}")
        print(f"   Reason: {status['reason']}")
        print(f"   Used today: {status['used_today']:.1f}h")
        print(f"   Available today: {status['available_today']:.1f}h")
        print(f"   Banked hours: {status['banked_hours']:.1f}h")
        print(f"   Monthly usage: {status['monthly_used']:.1f}h / {status['monthly_limit']}h")
    
    if args.bank:
        current_banked = manager.data["banked_hours"]
        new_total = min(current_banked + args.bank, 60)
        actually_banked = new_total - current_banked
        
        manager.data["banked_hours"] = new_total
        manager.save_usage_data()
        
        print(f"🏦 Banked {actually_banked:.1f}h (Total: {new_total:.1f}h)")
    
    if args.reset_day:
        today = manager.get_today_key()
        manager.data["daily_usage"][today] = 0
        manager.save_usage_data()
        print("🔄 Today's usage reset to 0h")
    
    if args.reset_month:
        manager.data["daily_usage"] = {}
        manager.data["monthly_total"] = 0
        manager.save_usage_data()
        print("🔄 Monthly usage reset to 0h")

if __name__ == "__main__":
    main()