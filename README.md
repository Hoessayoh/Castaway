# 🎣 Castaway - Wooper's Ultimate Fishing Adventure

[![Python](https://img.shields.io/badge/Python-3.x-blue.svg)](https://www.python.org/)
[![Pygame](https://img.shields.io/badge/Pygame-2.x-green.svg)](https://www.pygame.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> A massively deep fishing RPG inspired by Pokemon's fishing mechanics and Shangri-La Frontier's hidden systems!

---

## 🌟 Overview

**Castaway** is an addictive 2D fishing simulator featuring the beloved Pokemon character **Wooper**. With **Pokemon-exact fishing mechanics**, a massive **collection system**, **hidden character stats**, **environmental effects**, and **endless progression**, this game is designed to keep you hooked for hundreds of hours!

### Why Play Castaway?

- ✨ **18 fish species** with shiny variants (36 total collectibles!)
- 🎮 **Authentic Pokemon fishing** (cast → "..." → "!" → catch)
- 📈 **Unlimited progression** with leveling and stat growth
- 🏆 **24+ achievements** with gold rewards
- 🎣 **7 fishing rods** to unlock and upgrade
- 🌦️ **Dynamic weather & time systems** affecting catches
- 📅 **Daily rewards & login streaks**
- 🔒 **10+ secret traits** to discover
- 📊 **Comprehensive statistics** tracking everything
- 💎 **Hidden depth** like Shangri-La Frontier

---

## 🚀 Installation

### Prerequisites
- Python 3.x
- pip (Python package installer)

### Setup
```bash
# Clone the repository
git clone https://github.com/yourusername/Castaway.git
cd Castaway

# Install dependencies
pip install -r requirements.txt

# Run the game
cd src
python main.py
```

---

## 🎮 Controls

| Key | Action |
|-----|--------|
| ↑↓←→ | Move Wooper |
| SPACE | Cast line / Reel in fish |
| C | Open Collection (Pokedex) |
| A | View Achievements |
| S | Open Rod Shop |
| T | View Statistics |
| P | Pause game |
| ESC | Return to menu |

---

## 🐟 Core Features

### Pokemon-Style Fishing
- **Exact Pokemon mechanics**: Cast → Wait ("...") → Bite ("!") → Quick reaction needed!
- **Visual bobber system** with physics
- **Timing-based catching** for Perfect Cast bonuses
- **Streak system** for consecutive catches

### Massive Fish Database
**18 Unique Species** across **6 Rarity Tiers**:

| Rarity | Spawn Rate | Species Count | Gold Range |
|--------|-----------|---------------|------------|
| Common | 50% | 4 | 10-20g |
| Uncommon | 25% | 4 | 35-50g |
| Rare | 15% | 3 | 75-90g |
| Epic | 7% | 3 | 120-180g |
| Legendary | 2.5% | 2 | 250-300g |
| **Mythic** | 0.5% | 3 | **500-1000g** |

### Shiny Variant System
- **1% base chance** (modifiable with rods & environment!)
- **2x gold** and **2x EXP**
- Unique color palettes
- Sparkle particle effects
- Separate collection tracking

### Progression Systems
- **Unlimited leveling** with exp from catches
- **7 fishing rods** to unlock (Basic → Mythic)
- **Hidden character stats**: Luck, Patience, Technique, Perception, Endurance
- **Secret affinities**: Water, Moon, Void
- **10+ unlockable traits** with powerful effects

### Environmental Mechanics (Shangri-La Frontier Style!)
**5 Weather Conditions**:
- Clear, Rain (+30% rarity), Storm (+100% rarity!)
- Fog (+50% rarity), **Aurora** (+200% rarity, 2% chance!)

**4 Times of Day**:
- Dawn, Day, Dusk, Night (+80% rarity!)

**4 Moon Phases**:
- New (Void Fish boost), Waxing, **Full Moon** (+200% shiny!), Waning

### Achievement System
**24+ Achievements** including:
- Catch milestones (10, 50, 100, 500 fish)
- Collection completion goals
- Shiny hunting challenges
- Rarity-specific achievements
- Economic milestones (1K, 10K, 100K, 1M gold!)
- Secret achievements (Quick Reflexes, Perfect Streak, etc.)

**Total Achievement Rewards**: 50,000+ gold!

### Daily Rewards & Streaks
- **Login bonuses** (gold + EXP)
- **Streak multipliers** (+15% per day, caps at 2x)
- **Milestone rewards**:
  - Day 7: +200g, +100 EXP
  - Day 30: +1000g, +500 EXP
  - Day 100: **+5000g, +2500 EXP**

### Statistics Tracking
Comprehensive stats including:
- Catch rates, shiny rates, perfect casts
- Rarity breakdowns
- Economic tracking
- Environmental stats (weather, time, moon)
- Rod usage statistics
- Time records (fastest/slowest catches)

---

## 🎨 Visual Polish

### Particle Effects
- **Catch explosions** (rarity-colored)
- **Shiny sparkles** (extra particles)
- **Level-up bursts** (golden fountain)
- **Achievement glows** (purple/gold)
- **Water splashes** & bobber ripples

### Animations
- Smooth bobber physics
- Pokemon-style "..." waiting
- "!" exclamation on bite
- Floating +EXP and +Gold text
- Pulsing UI elements
- Glowing notifications

---

## 🔒 Secret Systems

### Hidden Traits (Discoverable!)
- **Moonlight Fisher**: Catch 100 fish at night → 2x shiny during night
- **Perfect Cast**: 50 perfect casts → Guaranteed perfect every 10 casts
- **Void Seeker**: Catch 10 Void Fish → 3x Void Fish spawn rate
- **Shiny Master**: 100 shinies → +50% shiny chance permanently
- **Combo King**: 50-catch streak → Combo bonuses last 2x longer
- **Weather Sage**: Fish in all weathers → 2x weather bonuses
- **Rod Master**: 100 catches per rod → All rod stats +10%
- **Speedrunner**: 10 fish < 2min → -25% bite time
- **Patient Monk**: Wait 10min → +50 Patience permanently
- **Golden Touch**: 1M gold → +25% gold from all fish

### Lore & World Building
Discoverable lore about:
- Wooper's ancient fishing mastery
- Mythic fish origins and legends
- Void Fish dimensional mystery
- Aurora phenomenon
- Moon blessings
- Perfect cast secrets
- Rod crafting lore

---

## 📁 Project Structure

```
Castaway/
├── src/
│   ├── main.py              # Main game loop
│   ├── player.py            # Wooper + fishing mechanics
│   ├── fish.py              # Fish database (18 species)
│   ├── world.py             # Environment rendering
│   ├── ui.py                # HUD and interface
│   ├── collection.py        # Pokedex-style tracker
│   ├── achievements.py      # Achievement system (24+)
│   ├── progression.py       # Leveling & rod shop
│   ├── daily_rewards.py     # Login rewards & streaks
│   ├── particles.py         # Visual effects system
│   ├── statistics.py        # Comprehensive stat tracking
│   ├── hidden_systems.py    # Secret mechanics & lore
│   └── settings.py          # Game configuration
├── requirements.txt         # Python dependencies
├── README.md               # This file
└── GAME_FEATURES.md        # Detailed feature list
```

---

## 🎯 Gameplay Loop

1. **Cast** your line into the water
2. **Wait** for a fish (environmental bonuses active)
3. **React** to the bite notification ("!")
4. **Catch** fish → Gain gold & EXP
5. **Level up** → Unlock better rods
6. **Buy rods** → Catch rarer fish & more shinies
7. **Complete collection** → Unlock achievements
8. **Discover secrets** → Master hidden mechanics
9. **Login daily** → Build streaks → Earn massive rewards
10. **Master everything** → True completionist status

---

## 💎 Endgame Goals

### 100% Completion Checklist
- [ ] Catch all 18 species (normal variants)
- [ ] Catch all 18 species (shiny variants)
- [ ] Unlock all 24+ achievements
- [ ] Own all 7 fishing rods
- [ ] Reach level 50+
- [ ] Max all character stats (100 each)
- [ ] Discover all 10 secret traits
- [ ] Unlock all lore entries
- [ ] Earn 1,000,000 gold
- [ ] Achieve 100-day login streak
- [ ] Catch 500+ total fish
- [ ] Perfect 100% catch rate

**Estimated Time to 100%**: 50-100+ hours

---

## 🌟 Why This Game Is Addictive

✅ **"One more cast" factor** - Quick, satisfying gameplay loop
✅ **Clear progression** - Always something to work toward
✅ **Collection appeal** - Pokemon-style Pokedex completion
✅ **Hidden depth** - Secrets to discover for hardcore players
✅ **Daily engagement** - Login rewards keep you coming back
✅ **RNG excitement** - Thrill of shiny/mythic catches
✅ **Skill + Luck balance** - Both matter for success
✅ **Long-term goals** - Achievements, collection, stats
✅ **Visible progress** - Levels, rods, and stats grow
✅ **Completionist content** - For achievement hunters

---

## 🛠️ Technical Details

- **Engine**: Pygame 2.x
- **Language**: Python 3.x
- **FPS**: 60 (smooth gameplay)
- **Resolution**: 800x600 (scalable)
- **Save System**: JSON-based persistence
- **Particle System**: Custom-built effects engine
- **State Machine**: Robust fishing state management

---

## 🎮 Game Design Philosophy

Inspired by:
- **Pokemon** - Fishing mechanics, collection systems, top-down perspective
- **Stardew Valley** - UI aesthetic, progression feel
- **Shangri-La Frontier** - Hidden mechanics, secret systems, deep lore
- **Mobile gacha games** - Daily rewards, streaks, addictive loops

---

## 📊 Stats At A Glance

- **18** unique fish species
- **36** total collectibles (with shinies)
- **6** rarity tiers
- **7** fishing rods
- **24+** achievements
- **10+** secret traits
- **5** weather conditions
- **4** times of day
- **4** moon phases
- **50,000+** total achievement gold rewards
- **Unlimited** max level
- **100+** hours of content

---

## 🤝 Contributing

This is a personal project, but feedback and suggestions are welcome! Feel free to:
- Report bugs
- Suggest new fish species
- Propose secret mechanics
- Share your completion screenshots

---

## 📝 License

This project is licensed under the MIT License - see LICENSE file for details.

---

## 🙏 Credits

- **Character**: Wooper (Pokemon franchise © Nintendo/Game Freak)
- **Inspiration**: Pokemon, Stardew Valley, Shangri-La Frontier
- **Built with**: Python, Pygame
- **Created by**: [Your Name]

---

## 🎣 Happy Fishing!

*"The secret to fishing is not just catching fish... it's becoming one with the water itself."*
- Ancient Wooper Wisdom

**May your casts be perfect and your shinies be plenty!** ✨🐟✨
