#!/usr/bin/env python3
"""Build Hank Quill (Dwarf BM Hunter) PWA guide. Architecture mirrors gordan-paladin (pal-v14)."""
import json, html, re as _re
E = html.escape
IV = "https://www.icy-veins.com/wow-forever/beast-mastery-hunter-ranged-dps-pve-guide"
IVLW = "https://www.icy-veins.com/wow-forever/leatherworking"
IVPR = "https://www.icy-veins.com/wow-forever/professions-overview"
IVDW = "https://www.icy-veins.com/wow-forever/dwarf-race-guide"
TFE = "https://theforeverera.com/en/spells/hunter/levels/"
TFEP = "https://theforeverera.com/en/hunter-pets/"
TFET = "https://theforeverera.com/en/talents/hunter/"

# Talent plan 10-30. Talent picks from Icy Veins Forever BM "Level 30 Talent Build"; level-by-level ORDER is our plan.
TAL = {}
for i, lv in enumerate(range(10, 15)): TAL[lv] = ("Deadly Aspects", f"{i+1}/5", "BM · chance for a 30% haste buff for 12 sec (Icy Veins: take first)")
for i, lv in enumerate(range(15, 17)): TAL[lv] = ("Pathfinding", f"{i+1}/2", "BM · +6% run speed at 2/2 (no mount before 40)")
for i, lv in enumerate(range(17, 19)): TAL[lv] = ("Focused Fire", f"{i+1}/2", "BM · more damage for you and your pet while it's out")
TAL[19] = ("Improved Revive Pet", "1/2", "BM · stronger, more reliable Revive Pet")
TAL[20] = ("Bestial Swiftness", "1/1", "BM · faster pet; needed for Intimidation")
for i, lv in enumerate(range(21, 26)): TAL[lv] = ("Unleashed Fury", f"{i+1}/5", "BM · pet damage, also boosts hawks")
TAL[26] = ("Summon Hawk", "1/1", "BM · new core button: up to 2 hawks on your target")
for i, lv in enumerate(range(27, 30)): TAL[lv] = ("Ferocity", f"{i+1}/5", "BM · pet crit, also boosts hawks")
TAL[30] = ("Intimidation", "1/1", "BM · on-use pet stun, next pet attack +100% crit")

MILESTONE = {
 1: ["Dwarves start in Coldridge Valley, Dun Morogh. [games.gg Forever Dwarf guide]", "Before 10: get as many Auto Shots off as you can before mobs reach you, then Raptor Strike in melee. [Icy Veins]", "Starting zones drop a quest item that teaches a gathering profession, so Skinning can start early. [Icy Veins professions]"],
 10: ["Tame Beast, Call Pet, Feed Pet, Revive Pet unlock. Icy Veins calls the pet the best leveling tool in the game. Bears are a strong first pick (Swipe hits 3 targets).", "Talents open (one point per level).", "Leatherworking Journeyman (cap 150) needs character level 10 and skill 50. Skinning Expert (cap 225) needs level 10. [Icy Veins professions]"],
 20: ["Wailing Caverns: Venomstrike bow and the Fang set (e.g. Leggings of the Fang). [Icy Veins]", "Leatherworking Expert (cap 225) needs level 20 and skill 125. Alliance trainer: Telonis, Darnassus. [Icy Veins LW]"],
 25: ["Skinning Artisan (cap 300) needs level 25. [Icy Veins professions]"],
 30: ["Level-30 gear picks: Truthseeker's Bow (quest), Dusky Leather Armor (Leatherworking), Triprunner Dungarees (Gnomeregan quest), Armor Piercer (Razorfen Kraul). [Icy Veins]"],
 31: ["Icy Veins expects a respec into Bestial Wrath once you have 31 points. Builds past 30 aren't published."],
 35: ["Leatherworking Artisan (cap 300) needs level 35 and skill 200. Alliance trainer: Drakk Stonehand, Aerie Peak. [Icy Veins LW]"],
 40: ["Mounts: Icy Veins says none before 40. Riding cost and Dwarf mount vendor not confirmed for Forever.", "Bestial Wrath (BM talent) and Aspect of the Pack become available. [The Forever Era]"],
 60: ["Max level. Endgame talents and gear not published yet."],
}
ZONES = [(1,"Coldridge Valley / Dun Morogh"),(10,"Loch Modan"),(18,"Wetlands / Redridge Mountains"),(20,"Duskwood / Wetlands"),(25,"Ashenvale / Wetlands"),(30,"Hillsbrad / Alterac & beyond"),(40,"Stranglethorn / Arathi / Desolace"),(45,"Tanaris / Feralas / Hinterlands"),(50,"Un'Goro / Felwood / Searing Gorge"),(55,"Winterspring / Plaguelands")]
SPELLS = json.load(open("spells.json"))
ZICON = {"Coldridge":"_dunmorogh","Loch":"_lochmodan","Wetlands":"_wetlands","Duskwood":"_duskwood","Ashenvale":"_ashenvale","Hillsbrad":"_hillsbrad","Stranglethorn":"_stv","Tanaris":"_tanaris","Un'Goro":"_ungoro","Winterspring":"_winterspring"}
def icimg(key, cls="ic"):
    v = SPELLS.get(key)
    return f'<img class="{cls}" src="icons/spells/{v["i"]}.jpg" alt="" loading="lazy">' if v else ""
def zicon(z):
    for k, v in ZICON.items():
        if z.startswith(k): return icimg(v, "ic zi")
    return ""
def zone(lv):
    z = ZONES[0][1]
    for a, n in ZONES:
        if lv >= a: z = n
    return z

TR = {int(k): v for k, v in json.load(open("trainer.json")).items()}
def trainer_html(lv):
    sp = TR.get(lv)
    if not sp: return ""
    li = []
    for x in sp:
        kind = "New" if x["kind"] == "New ability" else x["kind"].replace("Rank ", "R")
        tags = ""
        for b in x.get("badges", []):
            if b == "New in Forever" or b == "New rank in Forever": tags += f' <span class="tg fv">{E(b)}</span>'
            elif b.startswith("Talent") or b.startswith("Needs"): tags += f' <span class="tg tl">{E(b)}</span>'
        li.append(f'<li><span class="k {"new" if kind=="New" else ""}">{kind}</span> {E(x["name"])}{tags}</li>')
    note = "Beta client data (build 1.60.1.70374), Lv 1-30 playable in the beta" if lv <= 30 else "Beta client data, not reachable in the beta (cap 30). May change at launch"
    cls = "" if lv <= 30 else " warn"
    return f'<div class="trn"><b>Trainer</b><ul>{"".join(li)}</ul><span class="src{cls}">{note}. <a href="{TFE}">The Forever Era</a></span></div>'
LEARN = {}
for _lv in sorted(TR):
    for _x in TR[_lv]:
        if _x["kind"] == "New ability": LEARN.setdefault(_x["name"], _lv)
ITEM = {"Food": 1, "Water": 1, "Hearthstone": 1, "Mount": 40}
# each slot: candidates in order (name[@level], unconfirmed); latest learned wins
BARS = {
 "top": [[("Raptor Strike@6",0),("Intimidation@30",0)], [("Wing Clip",0)], [("Disengage",0)], [("Multi-Shot",0)],
         [("Freezing Trap",0)], [("Feign Death",0)], [("Arcane Shot@26",0)]],
 "mid": [[("Raptor Strike",0),("Arcane Shot",0),("Summon Hawk@26",0)], [("Serpent Sting",0)], [("Hunter's Mark",0)], [("Auto Shot",0)],
         [("Concussive Shot",0)], [("Mend Pet",0)], [("Aimed Shot",0)]],
 "bot": [[("Food",0)], [("Water",0)], [("Feed Pet",0)], [("Revive Pet",0)], [("Call Pet",0)], [("Hearthstone",0)], [("Mount",1)]],
 "asp": [[("Aspect of the Monkey",0)], [("Aspect of the Hawk",0)], [("Aspect of the Cheetah",0)], [("Aspect of the Beast",0)],
         [("Aspect of the Pack",1)], [("Aspect of the Wild",1)], [("Track Beasts",0)]],
}
ROWS = (("top","Top"),("mid","Middle"),("bot","Bottom"),("asp","Aspect"))
def bars_at(lv):
    out = {}
    for r, slots in BARS.items():
        row = []
        for cands in slots:
            pick = None
            for nm, unc in cands:
                base, _, at = nm.partition("@")
                L = int(at) if at else ITEM.get(base, LEARN.get(base, 99))
                if L <= lv: pick = {"n": base, "u": unc}
            row.append(pick)
        out[r] = row
    return out
BARDATA = {lv: bars_at(lv) for lv in range(1, 61)}
def bar_changes(lv):
    a, b = BARDATA[lv], BARDATA.get(lv-1, {r: [None]*7 for r, _ in ROWS})
    ch = []
    for r, lab in ROWS:
        for i in range(7):
            if a[r][i] != b[r][i] and a[r][i]:
                ch.append(f'{lab} {i+1}: {a[r][i]["n"]}' + (" (unconfirmed)" if a[r][i]["u"] else ""))
    return ch
rows = []
for lv in range(1, 61):
    items = list(MILESTONE.get(lv, []))
    if lv in TAL:
        n, r, d = TAL[lv]
        tal = f'<div class="tal"><b>{E(n)}</b> <span class="rank">{r}</span><div class="eff">{E(d)}</div><span class="src">Icy Veins Lv30 build · point order: our plan</span></div>'
    elif lv > 30:
        tal = '<div class="tal unk"><b>Talent point</b><div class="eff">31-60 builds not published (beta cap 30). Will fill in at launch.</div><span class="src warn">Unannounced</span></div>'
    else:
        tal = ""
    lis = "".join(f'<li>{E(x)}</li>' for x in items)
    summ = TAL[lv][0] if lv in TAL else (items[0][:48] + ("…" if items and len(items[0])>48 else "") if items else (f"Trainer: {len(TR[lv])} new" if lv in TR else "No new spells"))
    bc = bar_changes(lv)
    rows.append(f'''<div class="row" data-lv="{lv}" id="lv{lv}">
 <div class="row-head"><button class="chk" aria-label="Mark level {lv} done" data-k="lv{lv}"></button>
  <span class="lv">{lv}</span><span class="sum">{'<span class="tb">Trainer</span> ' if lv in TR else ''}{E(summ)}</span><span class="zone">{E(zone(lv))}</span></div>
 <div class="row-body">{("<div class=\"barch\"><b>Bars</b> " + " · ".join(E(c) for c in bc) + "</div>") if bc else ""}{trainer_html(lv)}{tal}<ul>{lis}</ul><div class="zline">{zicon(zone(lv))}Zone: {E(zone(lv))} <span class="src warn">(general Alliance path, unconfirmed for Forever)</span></div></div>
</div>''')

def ck(key, text, sub=""):
    s = f'<small>{sub}</small>' if sub else ""
    return f'<label class="ci"><input type="checkbox" data-k="{key}"><span>{text}{s}</span></label>'
talent_list = "".join(ck(f"t{lv}", f"<b>{lv}</b> · {E(TAL[lv][0])} {TAL[lv][1]}") for lv in range(10, 31))

PETS = json.load(open("pets.json"))
SHARED = []
for p in PETS:
    if p["slug"] == "wolf": SHARED = p["abilities"][3:]; p["abilities"] = p["abilities"][:3]
DIETN = {"raw-fish":"Raw Fish"}
COMMON = {"Bite","Claw","Dash","Dive"}
def pet_card(p):
    sig = [a for a in p["abilities"] if a["n"] not in COMMON]
    others = [a["n"] for a in p["abilities"] if a["n"] in COMMON]
    s = "".join(f'<li><img class="ic" src="icons/spells/{a["i"]}.jpg" alt="" loading="lazy"><b>{E(a["n"])}</b> <span class="src">{E(a["sum"])}</span><br>{E(a["top"])}</li>' for a in sig)
    diet = ", ".join(DIETN.get(d, d.title()) for d in p["diet"])
    return f'<div class="card pet"><h3>{icimg("_pet_"+p["slug"])}{E(p["name"])}</h3><p><b>Diet:</b> {E(diet)}<br><b>Also:</b> {E(", ".join(others))}</p><ul class="pab">{s}</ul></div>'
pet_cards = "".join(pet_card(p) for p in PETS)
shared = "".join(f'<li><b>{E(a["n"])}</b> <span class="src">{E(a["sum"])}</span></li>' for a in SHARED)

PAGE = f'''<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>Hank Quill · BM Hunter</title>
<meta name="theme-color" content="#0b1526">
<meta name="apple-mobile-web-app-capable" content="yes"><meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="apple-mobile-web-app-title" content="Hank Quill">
<link rel="apple-touch-icon" href="icons/icon-180.png"><link rel="icon" href="icons/icon-192.png">
<link rel="manifest" href="manifest.webmanifest"><link rel="stylesheet" href="style.css">
</head><body>
<header class="bar">
 <div class="bar-top"><div class="who"><span class="crest">{icimg("_dwarf","ci1")}{icimg("_hunter","ci1")}{icimg("_bm","ci1")}</span><b>Hank Quill</b><span>Dwarf BM Hunter · Lv <span id="curLv">1</span></span></div>
  <div class="lvpick"><button id="lvDown" aria-label="Level down">−</button><select id="lvSel" aria-label="Current level"></select><button id="lvUp" aria-label="Level up">+</button></div></div>
 <button id="rotBtn" class="rotbtn" aria-expanded="false">🏹 Rotation <span id="rotTag"></span></button>
 <div id="rot" class="rot" hidden></div>
 <nav class="tabs"><a href="#guide">1-60</a><a href="#bars">Bars</a><a href="#bm">BM</a><a href="#pet">Pet</a><a href="#gear">Gear</a><a href="#prof">Profs</a><a href="#back">Break</a><a href="#me">Me</a></nav>
</header>
<main>
<section id="t-guide" class="tab"><h2>Leveling 1-60</h2>
 <p class="note">For the live game (launch Nov 4, likely RP ruleset). Tap a level to open it, check it off and it collapses. Trainer lists are info only. Levels 1-30 match the beta; 31-60 may change at launch.</p>
 <label class="ci inline"><input type="checkbox" id="hideDone"> <span>Hide finished levels</span></label>
 {''.join(rows)}
</section>

<section id="t-bars" class="tab"><h2>My Bars · Lv <span id="barLv"></span></h2>
 <p class="note"><b>Draft layout.</b> A starting point for you to adjust. Change the level in the top bar. Gold outline = new at this level. Dashed orange = unconfirmed.</p>
 <div id="barsBox"></div>
 <div class="card"><h3>Why this layout</h3><ul>
  <li><b>Key 1</b> is your most-pressed shot: Raptor Strike (1-5, melee before your pet), Arcane Shot (6-25), then Summon Hawk (26+, keep 2 hawks up). Summon Hawk shares its cooldown with Arcane Shot, so Arcane moves to Top 7.</li>
  <li><b>Middle</b> is the fight loop from the Icy Veins rotation: Serpent Sting, Hunter's Mark, Auto Shot, Concussive Shot, Mend Pet, Aimed Shot.</li>
  <li><b>Top</b> is clicked utility and escapes: Raptor Strike (then Intimidation at 30), Wing Clip, Disengage, Multi-Shot, Freezing Trap, Feign Death.</li>
  <li><b>Bottom</b> is out of combat: food, water, pet care, hearthstone, mount at 40.</li></ul></div>
 <div class="card"><h3>Not on bars</h3><p class="note">Dismiss Pet, Tame Beast, Beast Lore, Eyes of the Beast, Eagle Eye, Scare Beast, Distracting Shot, Mongoose Bite, Immolation Trap, Frost Trap, Explosive Trap, Rapid Fire, Volley, Flare, Scorpid Sting, Viper Sting, Lacerate, Tranquilizing Shot, Raptor Strike (from 30), other tracking (Humanoids, Undead, Hidden, Elementals, Demons, Giants, Dragonkin), Stoneform and Find Treasure (Dwarf racials). Bestial Wrath (40, BM talent) once a 31+ build is published. Other-tree talent spells (Deterrence, Counterattack, Trueshot Aura, Scatter Shot, Strider Kick, Sniper Shot) aren't in this build.</p></div>
 <p class="src">Learn levels from <a href="{TFE}">The Forever Era</a> beta client data. Summon Hawk (26) and Intimidation (30) are talents in this plan. Mount placement and Aspect of the Pack/Wild are past the beta cap.</p>
</section>

<section id="t-bm" class="tab"><h2>{icimg("_bm","hic")}Beast Mastery</h2>
 <div class="card"><h3>Talents to 30</h3>{talent_list}
 <p class="src">Picks from the Icy Veins Forever "Level 30 Talent Build": Deadly Aspects 5, Pathfinding 2, 4 flexible points (we use Focused Fire 2, Improved Revive Pet 1, Bestial Swiftness 1), Unleashed Fury 5, Summon Hawk, Ferocity 3, Intimidation. Intimidation needs Bestial Swiftness in Forever. Icy Veins doesn't print a level-by-level order, so check it in the <a href="{TFET}">Forever Era calculator</a>. Spare Legacy points: Ferocity to 5, Bestial Discipline 2, Frenzy 1. <a href="{IV}">Icy Veins</a></p></div>
 <div class="card"><h3>Rotation</h3><ol>
  <li>Aspect of the Hawk up for fights. Aspect of the Cheetah while traveling (taking damage dazes you and drops it).</li>
  <li>Hunter's Mark on the target before the pull.</li>
  <li>Send your pet in first, abilities on auto-cast.</li>
  <li>Once the pet has hit it: Serpent Sting.</li>
  <li>Summon Hawk on cooldown, keeping 2 hawks up.</li>
  <li>Aimed Shot on cooldown. Multi-Shot instead against several mobs.</li>
  <li>Auto Shot the whole time.</li>
  <li>Pulled aggro off the pet? Disengage.</li>
  <li>Arcane Shot only when you're near full mana and 2 hawks will stay up for 6+ more seconds.</li></ol>
  <p>Out of mana? Keep Auto Shot and pet going. Spend mana on Mend Pet and Serpent Sting first.</p>
  <p class="src">Source: <a href="{IV}">Icy Veins Forever BM</a>.</p></div>
 <div class="card"><h3>Pet handling</h3><ul>
  <li>Let the pet build threat before you open. If you pull aggro, wait longer before shooting next time. Staying at range is faster than meleeing.</li>
  <li>Skin the last kill while the pet starts on the next mob.</li>
  <li>Mend Pet to heal it, Revive Pet if it dies (Improved Revive Pet makes this reliable in combat).</li>
  <li>Feign Death (30) drops threat on you, but mobs still go after a live pet nearby.</li>
  <li>In dungeons, control the pet so it doesn't pull extra packs.</li></ul>
  <p class="src"><a href="{IV}">Icy Veins Forever BM</a></p></div>
 <div class="card"><h3>Toolkit</h3><ul>
  <li>Freezing Trap locks down one target. Frost Trap slows a whole area.</li>
  <li>Concussive Shot is an instant single-target slow.</li>
  <li>Disengage lowers your threat.</li>
  <li>Tracking spells show mob types on the minimap.</li></ul>
  <p class="src"><a href="{IV}">Icy Veins Forever BM</a></p></div>
</section>

<section id="t-pet" class="tab"><h2>{icimg("_pet_bear","hic")}Your Pet</h2>
 <div class="card"><h3>Taming (from Lv 10)</h3><ul>
  <li>Every pet is <b class="nolink">Ferocity, Cunning, or Tenacity</b>. Type has no built-in damage bonus or penalty.</li>
  <li>Pets <b>inherit some of your stats</b>, so they scale with your gear.</li>
  <li><b>Happiness and loyalty still exist.</b> Feed your pet.</li>
  <li>Each family has its own unique ability.</li>
  <li><b>Leveling pet abilities:</b> tame a higher-level beast that already knows the rank you want. Your pet won't learn higher ranks on its own. Once learned, you can teach that rank to any other pet that can use it.</li>
  <li><b>Good leveling pick:</b> a Bear. It tanks well, and Swipe (5 sec cooldown) hits several enemies, so it holds threat on groups.</li></ul>
  <p class="src"><a href="{IV}">Icy Veins Forever BM</a>. Which beasts are tameable and where isn't in the client data.</p></div>
 <div class="card"><h3>Abilities every pet has</h3><ul>{shared}</ul><p class="src"><a href="{TFEP}">The Forever Era</a></p></div>
 <h3 class="sub">Families: diet and signature abilities</h3>
 {pet_cards}
 <p class="src">18 families from <a href="{TFEP}">The Forever Era</a> (beta client build 1.60.1.70374). Shown: each ability's top rank. Fox is new in Forever.</p>
</section>

<section id="t-gear" class="tab"><h2>Gear & Stats</h2>
 <div class="card"><h3>Stat priority (Icy Veins, beta Lv30)</h3><ol>
  <li><b>Weapon damage</b>: your #1 stat. Slower ranged weapons hit harder per shot, and Aimed Shot scales off weapon damage.</li>
  <li>Hit (rare on low-level gear)</li><li><b>Agility</b>: attack power and crit. Want it on every piece.</li><li>Crit (your pet inherits it)</li>
  <li>Intellect (1 AP per point with Careful Aim, plus mana)</li><li>Spirit (leveling regen only)</li><li>Stamina</li></ol>
  <p class="src"><a href="{IV}">Icy Veins Forever BM</a></p></div>
 <div class="card"><h3>{icimg("_dwarf")}Dwarf racials in Forever</h3><ul>
  <li><b>Gun Specialization is gone.</b> No gun bonus in Forever.</li>
  <li><b>Mace Specialization:</b> +1% crit while wielding a mace or two-handed mace. Whether a melee-slot mace counts for your shots is unconfirmed.</li>
  <li><b>Big Game Hunter:</b> +5% damage to Beasts.</li>
  <li><b>Stoneform:</b> removes and blocks Bleed, Poison and Disease, and cuts physical damage taken by 10% for 8 sec (3 min cooldown).</li>
  <li><b>Find Treasure:</b> now works alongside other tracking.</li></ul>
  <p class="src"><a href="{IVDW}">Icy Veins Dwarf race guide</a>. Icy Veins' own Alliance pick for BM is Human. Dwarf is fine.</p></div>
 <div class="card"><h3>Upgrades to look for</h3><ul>
  <li><b>Around 20:</b> Wailing Caverns: Venomstrike bow, Fang set (Leggings of the Fang).</li>
  <li><b>Around 30:</b> Truthseeker's Bow (quest), Dusky Leather Armor (Leatherworking), Triprunner Dungarees (Gnomeregan quest), Armor Piercer (Razorfen Kraul).</li>
  <li><b>Quiver or ammo pouch</b> (Leatherworking): faster ranged attacks. Light Leather Quiver for arrows, Small Leather Ammo Pouch for bullets.</li></ul>
  <p class="src"><a href="{IV}">Icy Veins BM</a>, <a href="{IVLW}">Icy Veins Leatherworking</a></p></div>
 <div class="card"><h3>Consumables</h3><ul><li>Best food and water you can get, plus health potions.</li><li>Elixir of Agility once you have spare gold.</li><li>Bandages from First Aid.</li><li>Sit at campfires you see for free buffs.</li></ul><p class="src"><a href="{IV}">Icy Veins BM</a></p></div>
</section>

<section id="t-prof" class="tab"><h2>Professions</h2>
 <div class="card"><h3>{icimg("_skinning")}Skinning + {icimg("_lw")}Leatherworking ✔</h3><p>Icy Veins' most natural early combo for Hunters: you kill beasts back to back, and you can skin while your pet opens on the next one. Leatherworking turns it into leather and mail armor, armor kits, quivers and ammo pouches, and bags.</p>
 <table><tr><td><b>Rank</b></td><td><b>Cap</b></td><td><b>LW needs</b></td><td><b>Skinning needs</b></td></tr>
 <tr><td>Apprentice</td><td>75</td><td>-</td><td>-</td></tr><tr><td>Journeyman</td><td>150</td><td>skill 50, Lv 10</td><td>skill 50</td></tr><tr><td>Expert</td><td>225</td><td>skill 125, Lv 20</td><td>skill 125, Lv 10</td></tr><tr><td>Artisan</td><td>300</td><td>skill 200, Lv 35</td><td>skill 200, Lv 25</td></tr></table>
 <p><b>Alliance LW trainers:</b> 1-75 Gretta Finespindle (Ironforge) and others; 75-150 Fimble Finespindle (Ironforge); 150-225 Telonis (Darnassus); 225-300 Drakk Stonehand (Aerie Peak).</p>
 <p><b>Campsite items:</b> LW Camp Tent (skill 20, rested XP up to 5% of a level), Tanning Rack (140), Sewing Machine (300). Skinning: Camp Chair (+2% crit), Field Guide (Track Beasts), Trapper's Workbench (a trap). All camp features share a 1-hour cooldown.</p>
 <p class="src"><a href="{IVLW}">Icy Veins Leatherworking</a>, <a href="{IVPR}">Icy Veins professions overview</a></p></div>
 <div class="card"><h3>{icimg("_cooking")}Cooking + {icimg("_firstaid")}First Aid</h3><ul><li><b>Cooking:</b> some foods give stats <b>and extra XP from kills</b>. Cooking also makes the campfire kits for campsites.</li><li><b>First Aid:</b> bandages, plus healing potions without Alchemy. Icy Veins says to keep it current while leveling.</li></ul>
 <p class="src"><a href="{IVPR}">Icy Veins professions</a>, <a href="{IV}">Icy Veins BM</a>. The exact XP bonus isn't on these pages.</p></div>
</section>

<section id="t-back" class="tab"><h2>Back from a break</h2>
 <div class="card big"><h3>30-second rotation</h3><ol>
  <li>Aspect of the Hawk on. Cheetah only for travel.</li><li>Hunter's Mark, send the pet in.</li><li>Serpent Sting once the pet has threat.</li><li>Summon Hawk on cooldown (2 up), Aimed Shot on cooldown, Auto Shot always.</li><li>Lost aggro: Disengage. Bad pull: Feign Death.</li><li>Between fights: Mend Pet, eat, drink, skin.</li></ol></div>
 <div class="card"><h3>Bag check</h3>
  {ck("b1","Arrows or bullets (plenty)")}{ck("b2","Pet food your pet's diet allows")}{ck("b3","Water")}{ck("b4","Food")}{ck("b5","Bandages / healing potions")}{ck("b6","Skinning knife")}{ck("b7","Hearthstone")}
  <div id="customBags"></div>
  <div class="addrow"><input id="bagNew" placeholder="Add an item…"><button id="bagAdd">Add</button></div>
  <button id="resetBags" class="ghost">Uncheck all</button></div>
 <div class="card"><h3>Notes</h3><textarea id="notes" rows="5" placeholder="Where I left off…"></textarea></div>
</section>

<section id="t-me" class="tab"><h2>{icimg("_dwarf","hic")}My Character</h2><div id="meBox">Loading…</div>
<div class="card credits"><h3>Credits</h3><p>Spell, item, class, race, pet and zone icons © Blizzard Entertainment, downloaded once from Wowhead's public icon CDN (wow.zamimg.com) and bundled in this app. Spell levels, pet data and spell/talent links: <a href="{TFE}" target="_blank" rel="noopener">The Forever Era</a>. Guides: <a href="{IV}" target="_blank" rel="noopener">Icy Veins</a>. Personal, non-commercial fan page; not affiliated with Blizzard.</p></div></section>
</main>
<script>window.SPELLS={json.dumps({k:v for k,v in SPELLS.items() if not k.startswith("_")})};window.BARS={json.dumps(BARDATA)};</script><script src="app.js"></script></body></html>'''
NAMES = sorted([k for k in SPELLS if not k.startswith("_") and SPELLS[k]["u"]], key=len, reverse=True)
NRX = _re.compile(r"(?<![\w'])(" + "|".join(_re.escape(n) for n in NAMES) + r")(?![\w'])")
def link(n):
    v = SPELLS[n]
    return f'<a class="sp" href="{v["u"]}" target="_blank" rel="noopener"><img class="ic" src="icons/spells/{v["i"]}.jpg" alt="" loading="lazy">{E(n)}</a>'
def linkify(doc):
    body_start = doc.index("<main>"); body_end = doc.index("</main>")
    head, body, tail = doc[:body_start], doc[body_start:body_end], doc[body_end:]
    out = []; st = []
    VOID = ("img","input","br","meta","link","hr")
    for part in _re.split(r"(<[^>]+>)", body):
        if part.startswith("<"):
            m = _re.match(r"<(/?)([a-z0-9]+)", part.lower())
            if m:
                tag = m.group(2)
                if m.group(1):
                    while st:
                        t2, _ = st.pop()
                        if t2 == tag: break
                elif tag not in VOID and not part.endswith("/>"):
                    t = part.lower()
                    st.append((tag, tag in ("a","textarea","option","script","button","pre","h3") or 'class="sum"' in t or 'class="row-head"' in t or 'class="pab"' in t or 'nolink' in t))
            out.append(part)
        else:
            out.append(part if any(f for _, f in st) else NRX.sub(lambda m: link(m.group(1)), part))
    return head + "".join(out) + tail
PAGE = linkify(PAGE)
open("index.html", "w").write(PAGE)
icons = sorted({v["i"] for v in SPELLS.values() if v["i"]} | {a["i"] for p in PETS for a in p["abilities"]} | {a["i"] for a in SHARED})
sw = open("sw.js").read()
sw = _re.sub(r"const C='[a-z]+-v\d+',F=\[[^\]]*\]", "const C='hq-v1',F=" + json.dumps(['./','index.html','style.css','app.js','data.json','manifest.webmanifest','icons/icon-180.png','icons/icon-192.png','icons/icon-512.png'] + [f"icons/spells/{i}.jpg" for i in icons]), sw)
open("sw.js","w").write(sw)
open("icons.txt","w").write("\n".join(icons))
print("built", len(PAGE))
