import sys

# --- Constants & Mappings ---
LEVEL_MAP = {'U': 0, 'C': 1, 'S': 2, 'TS': 3}
INV_LEVEL_MAP = {0: 'U', 1: 'C', 2: 'S', 3: 'TS'}

class Subject:
    def __init__(self, name, max_lvl, start_lvl):
        self.name = name
        self.max_lvl = LEVEL_MAP[max_lvl]
        self.start_lvl = LEVEL_MAP[start_lvl]
        self.curr_lvl = self.start_lvl

class Object:
    def __init__(self, name, lvl):
        self.name = name
        self.lvl = LEVEL_MAP[lvl]

class BLPSystem:
    def __init__(self):
        self.subjects = {}
        self.objects = {}
        self.setup_default_state()

    def setup_default_state(self):
        """Initializes the environment based on Lab requirements."""
        self.subjects.clear()
        self.objects.clear()
        self.add_subject("alice", "S", "U")
        self.add_subject("bob", "C", "C")
        self.add_subject("eve", "U", "U")
        
        self.add_object("pub.txt", "U")
        self.add_object("emails.txt", "C")
        self.add_object("username.txt", "S")
        self.add_object("password.txt", "TS")

    def add_subject(self, name, max_lvl, start_lvl):
        if LEVEL_MAP[start_lvl] > LEVEL_MAP[max_lvl]:
            print(f"> ERROR: {name} starting level cannot exceed max clearance.")
            return
        self.subjects[name] = Subject(name, max_lvl, start_lvl)

    def add_object(self, name, lvl):
        self.objects[name] = Object(name, lvl)

    def validate_levels(self, subject_name, object_name):
        """Returns True if current level EXACTLY matches object level."""
        sub = self.subjects[subject_name]
        obj = self.objects[object_name]
        return sub.curr_lvl == obj.lvl

    def set_level(self, subject_name, new_lvl_str):
        print(f"> Action: {subject_name} SET LEVEL to {new_lvl_str}...")
        sub = self.subjects[subject_name]
        new_lvl = LEVEL_MAP[new_lvl_str]
        
        # Constraint: Cannot lower below current, nor raise above max
        if new_lvl < sub.curr_lvl:
            print(f"> DENY: Cannot lower level below current operating level ({INV_LEVEL_MAP[sub.curr_lvl]}).")
        elif new_lvl > sub.max_lvl:
            print(f"> DENY: Cannot raise level above max clearance ({INV_LEVEL_MAP[sub.max_lvl]}).")
        else:
            sub.curr_lvl = new_lvl
            print(f"> ALLOW: {subject_name}'s level is now {new_lvl_str}.")

    def read(self, subject_name, object_name):
        print(f"> Action: {subject_name} READ {object_name}...")
        sub = self.subjects[subject_name]
        obj = self.objects[object_name]

        # Simple Security Property (No Read Up)
        if obj.lvl <= sub.max_lvl:
            print(f"> ALLOW: Obj Lvl ({INV_LEVEL_MAP[obj.lvl]}) <= Subj Max ({INV_LEVEL_MAP[sub.max_lvl]}).")
            # Dynamic Leveling
            if obj.lvl > sub.curr_lvl:
                print(f"> INFO: Raising {subject_name}'s current level to {INV_LEVEL_MAP[obj.lvl]}.")
                sub.curr_lvl = obj.lvl
        else:
            print(f"> DENY: Obj Lvl ({INV_LEVEL_MAP[obj.lvl]}) > Subj Max ({INV_LEVEL_MAP[sub.max_lvl]}). No Read Up.")

    def write(self, subject_name, object_name):
        print(f"> Action: {subject_name} WRITE {object_name}...")
        sub = self.subjects[subject_name]
        obj = self.objects[object_name]

        # *-Property (No Write Down)
        if sub.curr_lvl <= obj.lvl:
            print(f"> ALLOW: Subj Curr ({INV_LEVEL_MAP[sub.curr_lvl]}) <= Obj Lvl ({INV_LEVEL_MAP[obj.lvl]}).")
        else:
            print(f"> DENY: Subj Curr ({INV_LEVEL_MAP[sub.curr_lvl]}) > Obj Lvl ({INV_LEVEL_MAP[obj.lvl]}). No Write Down.")

    def print_state(self):
        print("\n--- Current BLP State ---")
        for name, sub in self.subjects.items():
            print(f"[Subject] {name}: Curr={INV_LEVEL_MAP[sub.curr_lvl]}, Max={INV_LEVEL_MAP[sub.max_lvl]}")
        for name, obj in self.objects.items():
            # Aligning text for clean output
            print(f"[Object]  {name:<13}: Lvl={INV_LEVEL_MAP[obj.lvl]}")
        print("-------------------------\n")


def run_case(sys, case_num):
    print(f"\n=============== CASE #{case_num} ===============")
    print("[System] Initializing Default State...")
    sys.setup_default_state()
    
    if case_num == 1:
        sys.read("alice", "emails.txt")
    elif case_num == 2:
        sys.read("alice", "password.txt")
    elif case_num == 3:
        sys.read("eve", "pub.txt")
    elif case_num == 4:
        sys.read("eve", "emails.txt")
    elif case_num == 5:
        sys.read("bob", "password.txt")
    elif case_num == 6:
        sys.read("alice", "emails.txt")
        sys.write("alice", "pub.txt")
    elif case_num == 7:
        sys.read("alice", "emails.txt")
        sys.write("alice", "password.txt")
    elif case_num == 8:
        sys.read("alice", "emails.txt")
        sys.write("alice", "emails.txt")
        sys.read("alice", "username.txt")
        sys.write("alice", "emails.txt")
    elif case_num == 9:
        sys.read("alice", "username.txt")
        sys.write("alice", "emails.txt")
        sys.read("alice", "password.txt")
        sys.write("alice", "password.txt")
    elif case_num == 10:
        sys.read("alice", "pub.txt")
        sys.write("alice", "emails.txt")
        sys.read("bob", "emails.txt")
    elif case_num == 11:
        sys.read("alice", "pub.txt")
        sys.write("alice", "username.txt")
        sys.read("bob", "username.txt")
    elif case_num == 12:
        sys.read("alice", "pub.txt")
        sys.write("alice", "password.txt")
        sys.read("bob", "password.txt")
    elif case_num == 13:
        sys.read("alice", "pub.txt")
        sys.write("alice", "emails.txt")
        sys.read("eve", "emails.txt")
    elif case_num == 14:
        sys.read("alice", "emails.txt")
        sys.write("alice", "pub.txt")
        sys.read("eve", "pub.txt")
    elif case_num == 15:
        sys.set_level("alice", "S")
        sys.read("alice", "username.txt")
    elif case_num == 16:
        sys.read("alice", "emails.txt")
        sys.set_level("alice", "U")
        sys.write("alice", "pub.txt")
        sys.read("eve", "pub.txt")
    elif case_num == 17:
        sys.read("alice", "username.txt")
        sys.set_level("alice", "C")
        sys.write("alice", "emails.txt")
        sys.read("eve", "emails.txt")
    elif case_num == 18:
        sys.read("eve", "pub.txt")
        sys.read("eve", "emails.txt")
    else:
        print("Invalid Case Number.")
        
    sys.print_state()


def main():
    blp = BLPSystem()
    
    while True:
        print("=========================================================")
        print(" Bell-LaPadula (BLP) Simulator CLI")
        print("=========================================================")
        print("\nOptions:")
        print("  [1-18] Run a specific test case (1 to 18)")
        print("  [A] Run all test cases sequentially")
        print("  [Q] Quit\n")
        
        choice = input("Enter choice: ").strip().upper()
        
        if choice == 'Q':
            print("Exiting...")
            sys.exit(0)
        elif choice == 'A':
            for i in range(1, 19):
                run_case(blp, i)
        elif choice.isdigit() and 1 <= int(choice) <= 18:
            run_case(blp, int(choice))
        else:
            print("Invalid input. Try again.")

if __name__ == "__main__":
    main()