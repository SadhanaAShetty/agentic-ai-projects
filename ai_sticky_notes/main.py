
from fastmcp import FastMCP
from pathlib import Path

mcp = FastMCP("AI Sticky Notes")

STORAGE_DIR = Path(__file__).resolve().parent
NOTES_FILE = STORAGE_DIR / "notes.txt"

def ensure_file():
    STORAGE_DIR.mkdir(parents=True, exist_ok=True)
    NOTES_FILE.touch(exist_ok=True)

ensure_file()


@mcp.tool
def add_note(note: str) -> str:
    """
    Add a note to the sticky notes.

    Args:
        note: The note to be added.

    Returns:
        Confirmation message.
    """
    if not note.strip():
        raise ValueError("Note cannot be empty.")

    ensure_file()

    with NOTES_FILE.open("a", encoding="utf-8") as f:
        f.write(note.strip() + "\n")

    return "Note added successfully."


@mcp.tool
def read_notes() -> str:
    """Read all saved sticky notes."""
    ensure_file()

    with NOTES_FILE.open("r", encoding="utf-8") as f:
        notes = f.read()

    return notes if notes.strip() else "No notes found."


@mcp.tool
def delete_notes() -> str:
    """Delete all saved sticky notes."""
    ensure_file()
    NOTES_FILE.write_text("", encoding="utf-8")
    return "All notes deleted successfully."


@mcp.resource("notes://latest")
def get_latest_note() -> str:
    """Get the latest saved sticky note."""
    ensure_file()

    with NOTES_FILE.open("r", encoding="utf-8") as f:
        notes = f.readlines()

    if not notes:
        return "No notes found."

    return notes[-1].strip()


@mcp.prompt
def notes_summary_prompt() -> str:
    """Generate a summary of all saved sticky notes."""
    notes = read_notes()
    if not notes.strip():
        return "No notes found."

    return f"Here is a summary of your sticky notes:\n{notes}"

if __name__ == "__main__":
    mcp.run()
