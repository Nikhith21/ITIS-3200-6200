# BLP Access Control Visualizer

A Python CLI simulation of the Bell-LaPadula (BLP) access control model. This was built for Lab 5 to demonstrate state transitions, access evaluations, and the core confidentiality properties of BLP. 

## Core Security Properties Enforced
* **Simple Security Property (No Read Up):** A subject cannot read an object with a higher classification level than their maximum clearance.
* **Dynamic Leveling:** If a subject reads an object classified higher than their *current* operating level (but within their max clearance), their current level is automatically raised to match the object.
* ***-Property (No Write Down):** A subject cannot write to an object with a lower classification level than their *current* operating level.

## Environment Setup
The simulation initializes with the following default state:

**Subjects:**
* `alice`: Max = S (Secret), Start = U (Unclassified)
* `bob`: Max = C (Classified), Start = C (Classified)
* `eve`: Max = U (Unclassified), Start = U (Unclassified)

**Objects:**
* `pub.txt`: U
* `emails.txt`: C
* `username.txt`: S
* `password.txt`: TS (Top Secret)

## Usage
Run the script via terminal:
`python blp_model.py`

From the CLI menu, you can run any of the 18 predefined Lab 5 test cases individually to view the state transitions, or execute them all sequentially.

## Academic Integrity & AI Disclaimer
* Generative AI tools were used as an assistant during the development of this project for brainstorming and clarifying access control models.
* All code executions, test case evaluations, and logic implementation were performed, reviewed, and understood by the author.
* The results and logic are based on a direct understanding of the BLP security properties. I take full responsibility for the correctness of the operations and the conclusions presented in this code.
