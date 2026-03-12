import random
import pandas as pd # with openpyxl
import json
import os
import sys

path = "AwDangitData.xlsx" # the spreadsheet file should be in the same working directory
savefile = "character.json" # the save file should also be in the same working directory

class Character:
    def __init__(self, name):
        self.name = name
        self.spins = 0
        self.stats = {
            "VIT": 0,
            "STR": 0,
            "DEX": 0,
            "INT": 0,
            "SEN": 0,
            "CHA": 0
        }
        self.blessings = []
        self.curses = []
    
    def rename(self):
        newname = input("What is this character's new name?\n")
        self.name = newname
    def give_spin(self):
        self.spins += 1
    def print_sheet(self):
        print("\n________________________________")
        print("Name:", self.name)
        print("Spins:", self.spins)

        print("Stats:")
        for k, v in self.stats.items():
            print(f"\t{k}: {v}")

        print("Blessings:")
        if self.blessings:
            for b in self.blessings:
                name = b.get("Name", "Unknown")
                potency = b.get("Potency", "?")
                desc = b.get("Description", "No description.")
                print(f"\t- {name} (Potency: {potency})")
                print(f"\t  {desc}")
        else:
            print("\tNone")

        print("Curses:")
        if self.curses:
            for c in self.curses:
                name = c.get("Name", "Unknown")
                potency = c.get("Potency", "?")
                desc = c.get("Description", "No description.")
                print(f"\t- {name} (Potency: {potency})")
                print(f"\t  {desc}")
        else:
            print("\tNone")

        print("________________________________\n")
    
    def addeffect(self, bless, alpha=2.0): # alpha controls how strongly low potency is favored
        import numpy as np
        dfs = pd.read_excel(path, sheet_name=["Blessings", "Curses"])
        sheet = "Blessings" if bless else "Curses"
        if sheet == "Blessings":
            alpha=1.8
        else:
            alpha=2.0
        df = dfs[sheet].copy()
        if df.empty:
            print("No effects found.")
            return
        # Ensure Potency is numeric
        df["Potency"] = pd.to_numeric(df["Potency"], errors="coerce")
        df = df.dropna(subset=["Potency"])
        if df.empty:
            print("No valid potency values.")
            return
        pot = df["Potency"].values
        # Power-based weighting (bias toward lower potency)
        maxp = pot.max()
        weights = (maxp - pot + 1e-6) ** alpha
        probs = weights / weights.sum()
        # Select row
        chosen_idx = np.random.choice(len(df), p=probs)
        chosen_row = df.iloc[chosen_idx]
        # Store full row as dict
        effect = chosen_row.to_dict()
        if bless:
            self.blessings.append(effect)
            print("Added blessing:", effect.get("Name", "Unknown"))
        else:
            self.curses.append(effect)
            print("Added curse:", effect.get("Name", "Unknown"))
    
    def removeeffect(self, curse):
        effects = self.curses if curse else self.blessings
        label = "curse" if curse else "blessing"
        if not effects:
            print(f"No {label}s to remove.")
            return
        print(f"Select a {label} to remove:")
        for i, e in enumerate(effects, start=1):
            name = e.get("Name", "Unknown")
            potency = e.get("Potency", "?")
            print(f"\t{i}. {name} (Potency: {potency})")
        choice = input("Enter number to remove (or press Enter to cancel): ").strip()
        if not choice:
            print("Cancelled.")
            return
        if not choice.isdigit():
            print("Invalid selection.")
            return
        idx = int(choice) - 1
        if 0 <= idx < len(effects):
            removed = effects.pop(idx)
            print(f"Removed {label}: {removed.get('Name', 'Unknown')}")
        else:
            print("Invalid selection.")

    def statmod(self, increase):
        amt = 0
        if increase:
            amt = random.randint(1,10)
        else:
            amt = random.randint(1,5)
        print("Amount: ", amt)
        response = input("Which stat? (VIT/STR/DEX/INT/SEN/CHA)\n").strip().upper()
        if response in self.stats:
            self.stats[response] += amt if increase else -amt
        else:
            print("Unrecognized stat.")

    def spin(self):
        if self.spins <= 0:
            print("Not enough spins.")
            return
        self.spins -= 1
        print("Spinning...")
        good = random.choice([True, False])
        # Weights (relative; only the ratios matter)
        # For bad-outcome actions when blessings exist:
        #   stat decrease : 4
        #   add curse     : 4  <- this weight will match remove-curse below
        #   remove bless  : 2  <- less likely
        BAD_WEIGHTS_FULL = {"stat": 4, "add": 4, "remove": 2}
        # For good-outcome actions when curses exist:
        #   stat increase : 4
        #   add bless     : 2
        #   remove curse  : 4  <- matches add-curse above
        GOOD_WEIGHTS_FULL = {"stat": 4, "add": 2, "remove": 4}
        if good:
            print("Outcome: Good")
            # If no curses, give simpler 50/50 stat increase or add blessing
            if not self.curses:
                action = random.choices(["stat", "add"], weights=[1, 1], k=1)[0]
                if action == "stat":
                    print("Stat increase")
                    self.statmod(True)
                else:
                    print("Add blessing")
                    self.addeffect(True)
            else:
                # use full weighted set: stat increase / add blessing / remove curse
                actions = ["stat", "add", "remove"]
                weights = [GOOD_WEIGHTS_FULL[a] for a in actions]
                action = random.choices(actions, weights=weights, k=1)[0]
                if action == "stat":
                    print("Stat increase")
                    self.statmod(True)
                elif action == "add":
                    print("Add blessing")
                    self.addeffect(True)
                else:  # remove
                    print("Remove curse")
                    self.removeeffect(True)
        else:
            print("Outcome: Bad")
            # If no blessings, keep 50/50 stat decrease or add curse
            if not self.blessings:
                action = random.choices(["stat", "add"], weights=[1, 1], k=1)[0]
                if action == "stat":
                    print("Stat decrease")
                    self.statmod(False)
                else:
                    print("Add curse")
                    self.addeffect(False)
            else:
                # use full weighted set: stat decrease / add curse / remove blessing
                actions = ["stat", "add", "remove"]
                weights = [BAD_WEIGHTS_FULL[a] for a in actions]
                action = random.choices(actions, weights=weights, k=1)[0]
                if action == "stat":
                    print("Stat decrease")
                    self.statmod(False)
                elif action == "add":
                    print("Add curse")
                    self.addeffect(False)
                else:  # remove
                    print("Remove blessing")
                    self.removeeffect(False)
        self.print_sheet()
    
    def to_dict(self):
        """Return a JSON-serializable dict representing this character."""
        return {
            "name": self.name,
            "spins": int(self.spins),
            "stats": {k: int(v) for k, v in self.stats.items()},
            "blessings": [dict(b) for b in self.blessings],
            "curses": [dict(c) for c in self.curses],
        }

    @classmethod
    def from_dict(cls, data):
        """Create a Character from a dict (produced by to_dict)."""
        c = cls(data.get("name", "Unnamed"))
        c.spins = int(data.get("spins", 0))
        # load stats (ensure keys exist)
        stats = data.get("stats", {})
        for k in c.stats:
            c.stats[k] = int(stats.get(k, 0))
        # copy lists of dicts
        c.blessings = [dict(b) for b in data.get("blessings", [])]
        c.curses = [dict(cu) for cu in data.get("curses", [])]
        return c

    def save(self, filename):
        """Save this character to a JSON file."""
        try:
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(self.to_dict(), f, ensure_ascii=False, indent=2)
            print(f"Saved {self.name} -> {filename}")
        except Exception as e:
            print("Save failed:", e)

    @classmethod
    def load(cls, filename):
        """Load a Character from a JSON file and return the instance."""
        if not os.path.exists(filename):
            raise FileNotFoundError(filename)
        try:
            with open(filename, "r", encoding="utf-8") as f:
                data = json.load(f)
            return cls.from_dict(data)
        except Exception as e:
            raise RuntimeError(f"Failed to load {filename}: {e}")

    # Optional helpers for multiple characters in one file
    @staticmethod
    def save_all(char_list, filename):
        """Save a list of Characters to a single JSON file as a dict name->data."""
        payload = {c.name: c.to_dict() for c in char_list}
        try:
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(payload, f, ensure_ascii=False, indent=2)
            print(f"Saved {len(char_list)} characters -> {filename}")
        except Exception as e:
            print("Save all failed:", e)

    @staticmethod
    def load_all(filename):
        """Load multiple characters saved by save_all; returns list of Character."""
        if not os.path.exists(filename):
            raise FileNotFoundError(filename)
        with open(filename, "r", encoding="utf-8") as f:
            payload = json.load(f)
        chars = []
        for name, data in payload.items():
            chars.append(Character.from_dict(data))
        return chars

if __name__ == "__main__":
    char = Character("noname")
    stop = False
    while not stop:
        userin = input("load to load previous character, new to create new character (saving new overwrites previous), exit to exit\n")
        if userin == "new":
            stop = True
        elif userin == "load":
            char = Character.load(savefile)
            stop = True
        elif userin == "exit":
            stop = True
            sys.exit()
        else:
            print("Invalid input\n")
    stop = False
    while not stop:
        userin = input("exit to save and exit, print to print char sheet, spin to spin, rename to rename, givespin to increase spins\n")
        if userin == "exit":
            char.save(savefile)
            stop = True
            sys.exit()
        elif userin == "print":
            char.print_sheet()
        elif userin == "spin":
            char.spin()
        elif userin == "rename":
            char.rename()
        elif userin == "givespin":
            char.give_spin()
        else:
            print("Invalid input\n")