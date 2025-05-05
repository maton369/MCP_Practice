from mcp.server.fastmcp import FastMCP
import os
import pathlib
import sys

mcp = FastMCP("MCPPracticeFilesystem")

BASE_DIR = pathlib.Path(os.path.expanduser("~/MCP_Practice/Claude_Node.js")).resolve()


def _validate_path(rel_path: str) -> pathlib.Path:
    target = (BASE_DIR / rel_path).resolve()
    if not str(target).startswith(str(BASE_DIR)):
        raise ValueError(f"Access denied: {rel_path}")
    return target


@mcp.tool()
def list_items() -> list[dict]:
    """
    デスクトップ直下のファイル・フォルダ一覧を取得します。
    戻り値は [{'name': 'foo.txt', 'is_dir': False}, ...] の形式です。
    """
    items = []
    for p in BASE_DIR.iterdir():
        items.append({"name": p.name, "id_dir": p.is_dir()})
    return items


@mcp.tool()
def create(path: str, is_dir: bool = False) -> str:
    """
    デスクトップ上にフォルダまたはファイルを作成します。
    - path: デスクトップからの相対パス (例: 'hoge/README.md')
    - is_dir: True のときフォルダ、False のときファイルを作成
    """
    target = _validate_path(path)
    if is_dir:
        target.mkdir(parents=True, exist_ok=True)
        return f"Directory created: {target}"
    else:
        target.parent.mkdir(parents=True, exist_ok=True)
        target.touch(exist_ok=True)
        return f"File created: {target}"


@mcp.tool()
def append_to_file(path: str, content: str) -> str:
    """
    デスクトップ上の既存ファイルにテキストを追記します。
    - path: デスクトップからの相対パス (例: 'hoge/notes.txt')
    - content: 追記する文字列
    """
    target = _validate_path(path)
    if not target.exists():
        raise FileExistsError(f"File not found:{target}")
    if target.is_dir():
        raise IsADirectoryError(f"Is a directory: {target}")
    with open(target, "a", encoding="utf-8") as f:
        f.write(content)
    return f"Appended to {target}"


if __name__ == "__main__":
    mcp.run()
