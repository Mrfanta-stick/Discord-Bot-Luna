# ⏰ Understanding GitHub Codespace Hours

## 📊 **How the 180 Hours/Month Works**

### **What Counts as Usage:**
- ✅ **Codespace is RUNNING** (even if idle)
- ✅ **Terminal is open** (even if nothing is happening)
- ✅ **Browser tab is open** with Codespace

### **What DOESN'T Count:**
- ❌ Codespace is **stopped/sleeping**
- ❌ Browser tab is **closed** (after timeout)
- ❌ You're **offline** (after Codespace sleeps)

## 🎯 **Your Luna Bot Setup:**

### **Scenario 1: Bot Running 24/7 Non-Stop**
```
24 hours/day × 30 days = 720 hours/month ❌
This EXCEEDS your 180-hour limit!
```

### **Scenario 2: With Smart Usage Manager (Current Setup)**
```
6 hours/day × 30 days = 180 hours/month ✅
PERFECT! Exactly your limit!
```

### **Scenario 3: Codespace Sleeps After 4 Hours**
```
4 hours active + sleep + 4 hours active + sleep...
= ~120-150 hours/month ✅
SAFE! Under your limit!
```

## 🔑 **KEY INSIGHT:**

**Your 180 hours count CODESPACE RUNTIME, not bot activity!**

- **Interacting with Luna** (messages, commands): Does NOT count extra
- **Bot sitting idle**: Still counts if Codespace is running
- **No messages for 4 hours**: Codespace sleeps = stops counting hours

## 📈 **Current Setup Breakdown:**

### **With Your Smart Usage Manager:**

| Time | Codespace Status | Bot Status | Hours Used |
|------|-----------------|------------|------------|
| Hour 0-6 | Running | AI Responses (Ollama) | 6h/day |
| Hour 6+ | Running | Text Fallbacks | Still counts! |
| After 4h idle | Sleeping | Stopped | 0h/day |

### **Best Practice:**

```
✅ Let Codespace sleep after 4 hours of no activity
✅ It auto-wakes when someone messages Luna
✅ Auto-restart script brings Luna back online
✅ This keeps you well under 180h/month limit
```

## 🎯 **To Maximize Your Free Hours:**

### **Option A: Current Setup (Smart & Safe)**
- 4-hour timeout
- Auto-sleeps when idle
- Auto-restarts on wake
- **Usage**: ~120-150h/month ✅

### **Option B: Always-On (Will Exceed Limit)**
- No timeout
- Always running
- **Usage**: ~720h/month ❌ (4× your limit!)

### **Option C: Manual Control**
- Start when needed
- Stop when not in use
- **Usage**: Variable, you control it

## 💡 **Recommendation:**

**Keep your current setup!** It's perfect because:
1. ✅ 4-hour timeout saves hours
2. ✅ Smart usage manager (6h/day) adds safety buffer
3. ✅ Auto-restart keeps Luna available
4. ✅ Stays well under 180h/month limit

## 🔍 **Monitor Your Usage:**

### **Check Codespace Hours Used:**
1. Go to github.com
2. Settings → Billing → Codespaces
3. View current month usage

### **Check Bot Hours Used:**
```bash
# In Discord
/usage

# In Codespace terminal
python usage_admin.py --status
```

## 🚨 **What Happens If You Exceed 180h?**

With GitHub Student Pack:
- **180h free** included
- **After 180h**: Codespace stops automatically
- **Next month**: Resets to 180h again

**With current setup, you won't exceed it!** 🎉

---

## 📝 **Summary:**

**Question**: Does 180h end if I keep bot running without activity?
**Answer**: YES! Codespace runtime counts, not bot activity.

**Question**: Does it exhaust if I interact for 180h straight?
**Answer**: Interaction doesn't matter - only Codespace runtime counts.

**Your Setup**: Perfect! 4h timeout + auto-restart = ~120-150h/month ✅