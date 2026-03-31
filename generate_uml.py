#!/usr/bin/env python3
"""
Generate UML diagram as PNG from Mermaid syntax.
This script uses mermaid-cli to convert the diagram to PNG.
"""

import subprocess
import os
from pathlib import Path

# Define paths
project_dir = Path("/Users/rahul/Desktop/ai110-module2show-pawpal-starter")
html_file = project_dir / "uml_final.html"
output_png = project_dir / "uml_final.png"

# Mermaid diagram in code format
mermaid_code = '''
classDiagram
    class Owner {
        -name: str
        -pets: List~Pet~
        +addPet(pet: Pet): void
        +removePet(petName: str): bool
        +getPets(): List~Pet~
        +getAllTasks(includeCompleted: bool): List~Task~
    }

    class Pet {
        -name: str
        -species: str
        -age: int
        -tasks: List~Task~
        +addTask(task: Task): void
        +removeTask(taskDescription: str): bool
        +getTasks(): List~Task~
        +getPendingTasks(): List~Task~
    }

    class Task {
        -description: str
        -time_minutes: int
        -frequency: str
        -priority: int
        -is_completed: bool
        -scheduled_date: datetime | None
        -scheduled_time: str | None
        +markComplete(pet: Pet | None): void
        +markIncomplete(): void
    }

    class Scheduler {
        +generateDailyPlan(owner: Owner, availableTime: int): List~Task~
        +sortByPriority(tasks: List~Task~): List~Task~
        +detectConflicts(pet: Pet, newTask: Task): bool
        +addTaskWithConflictDetection(pet: Pet, newTask: Task): void
        +filterTasksByCompletion(owner: Owner, isCompleted: bool): List~Task~
        +filterTasksByPetName(owner: Owner, petName: str): List~Task~
        +collectPendingTasks(owner: Owner): List~Task~
    }

    Owner "1" *-- "0..*" Pet : manages
    Pet "1" *-- "0..*" Task : includes
    Scheduler ..> Owner : reads from
    Scheduler ..> Pet : checks conflicts for
    Scheduler ..> Task : prioritizes/filters
'''

def generate_png_with_graphviz():
    """Generate PNG using graphviz (if available)."""
    try:
        import graphviz
        
        # Create diagram
        graph = graphviz.Digraph(
            name='PawPal+ UML',
            comment='PawPal+ System UML Diagram',
            format='png',
            graph_attr={
                'rankdir': 'TB',
                'bgcolor': 'white',
                'fontname': 'Arial',
                'fontsize': '11',
            },
            node_attr={
                'shape': 'box',
                'style': 'filled',
                'fillcolor': '#E8F4F8',
                'fontname': 'Arial',
            }
        )
        
        # Add nodes
        graph.node('Owner', 'Owner\n\n- name: str\n- pets: List[Pet]\n\n+ addPet()\n+ removePet()\n+ getPets()\n+ getAllTasks()')
        graph.node('Pet', 'Pet\n\n- name: str\n- species: str\n- age: int\n- tasks: List[Task]\n\n+ addTask()\n+ removeTask()\n+ getTasks()\n+ getPendingTasks()')
        graph.node('Task', 'Task\n\n- description: str\n- time_minutes: int\n- frequency: str\n- priority: int\n- is_completed: bool\n- scheduled_date\n- scheduled_time\n\n+ markComplete()\n+ markIncomplete()')
        graph.node('Scheduler', 'Scheduler\n\n+ generateDailyPlan()\n+ sortByPriority()\n+ detectConflicts()\n+ addTaskWithConflictDetection()\n+ filterTasksByCompletion()\n+ filterTasksByPetName()\n+ collectPendingTasks()')
        
        # Add edges
        graph.edge('Owner', 'Pet', label='manages (1..*)')
        graph.edge('Pet', 'Task', label='includes (1..*)')
        graph.edge('Scheduler', 'Owner', label='reads from', style='dashed')
        graph.edge('Scheduler', 'Pet', label='checks conflicts', style='dashed')
        graph.edge('Scheduler', 'Task', label='prioritizes/filters', style='dashed')
        
        # Render
        output_path = str(project_dir / 'uml_final')
        graph.render(output_path, cleanup=True)
        print(f"✅ PNG generated: {output_path}.png")
        return True
        
    except ImportError:
        return False


def generate_png_with_mermaid_cli():
    """Generate PNG using mermaid-cli (if available)."""
    try:
        # Create temporary mermaid file
        mmd_file = project_dir / "temp_diagram.mmd"
        mmd_file.write_text(mermaid_code)
        
        # Run mmdc command
        result = subprocess.run(
            ['mmdc', '-i', str(mmd_file), '-o', str(output_png), '-b', 'white'],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            mmd_file.unlink()  # Clean up temp file
            print(f"✅ PNG generated with mermaid-cli: {output_png}")
            return True
        else:
            print(f"⚠️  mermaid-cli error: {result.stderr}")
            return False
            
    except FileNotFoundError:
        return False


def create_markdown_diagram():
    """Create a markdown file with the diagram code for manual conversion."""
    md_file = project_dir / "UML_DIAGRAM.md"
    
    content = f"""# PawPal+ UML Class Diagram

## Final Implementation (March 31, 2026)

Below is the Mermaid diagram code for the PawPal+ system:

```mermaid
{mermaid_code}
```

## Class Relationships

### Owner (1 to many Pet)
- An owner manages multiple pets
- Provides centralized access to all tasks across all pets via `getAllTasks()`

### Pet (1 to many Task)
- Each pet has associated care tasks
- Supports pending task filtering via `getPendingTasks()`

### Task (Atomic unit)
- Represents a single care activity
- Supports recurring patterns (daily/weekly)
- Tracks scheduling (date & time) and completion status

### Scheduler (Stateless utility)
- Orchestrates task scheduling without maintaining state
- Provides 7 methods for planning, filtering, and conflict detection

## Implementation Decisions

✅ **No ID fields:** Classes use natural keys (name, description) for simplicity
✅ **Scheduling flexibility:** Tasks track scheduled_time (HH:MM), scheduled_date, and frequency
✅ **Stateless Scheduler:** All parameters passed as method arguments
✅ **Conflict detection:** Time-based conflicts identified when scheduling tasks
✅ **Recurring tasks:** markComplete() auto-creates next occurrence if frequency is set
✅ **Multi-level filtering:** Filter by pet, completion status, priority, or available time

## Converting to PNG

You can convert this diagram to PNG using:

1. **Online:** Visit [Mermaid Live](https://mermaid.live) and paste the diagram code
2. **CLI:** Install mermaid-cli and run: `mmdc -i UML_DIAGRAM.md -o uml_final.png`
3. **Browser:** Open `uml_final.html` and click "Download as PNG"
"""
    
    md_file.write_text(content)
    print(f"✅ Markdown diagram created: {md_file}")
    return True


if __name__ == "__main__":
    print("🎨 Generating PawPal+ UML Diagram...")
    print()
    
    # Try graphviz first
    if generate_png_with_graphviz():
        print("✨ Success! Diagram generated using graphviz.")
    # Try mermaid-cli second
    elif generate_png_with_mermaid_cli():
        print("✨ Success! Diagram generated using mermaid-cli.")
    # Fallback to markdown
    else:
        print("⚠️  Graphviz and mermaid-cli not found.")
        print("Creating markdown version instead...")
        create_markdown_diagram()
        print("\n📋 Instructions:")
        print("1. Open uml_final.html in your browser to view the interactive diagram")
        print("2. Click 'Download as PNG' button to export as uml_final.png")
        print("   OR")
        print("3. Visit https://mermaid.live and paste the code from UML_DIAGRAM.md")
        print("4. Export as PNG from Mermaid Live")
