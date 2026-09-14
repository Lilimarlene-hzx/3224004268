import argparse
import sys
from difflib import SequenceMatcher
from pathlib import Path


def read_text(path: Path) -> str:
    """Read a UTF-8 text file, including files with a UTF-8 BOM."""
    if not path.is_absolute():
        raise ValueError(f"路径必须是绝对路径: {path}")
    if not path.exists():
        raise FileNotFoundError(f"文件不存在: {path}")
    if not path.is_file():
        raise OSError(f"路径不是有效的文件: {path}")
    try:
        return path.read_text(encoding="utf-8-sig")
    except (OSError, UnicodeError) as e:
        raise OSError(f"读取文件失败 {path}: {e}") from e


def plagiarism_rate(original: str, copy: str) -> float:
    """Return the normalized similarity between two papers."""
    if not original and not copy:
        return 1.0
    if not original or not copy:
        return 0.0
    return SequenceMatcher(None, original, copy, autojunk=False).ratio()


def main() -> None:
    parser = argparse.ArgumentParser(description="论文查重扩展版")
    parser.add_argument("original", type=Path, help="原文路径")
    parser.add_argument("copy", type=Path, help="抄袭版路径")
    parser.add_argument("answer", type=Path, help="结果输出路径")
    args = parser.parse_args()

    if not args.original.is_absolute() or not args.copy.is_absolute() or not args.answer.is_absolute():
        parser.error("原文、抄袭版和答案路径都必须是绝对路径")

    try:
        original_text = read_text(args.original)
        copy_text = read_text(args.copy)
        rate = plagiarism_rate(original_text, copy_text)

        args.answer.parent.mkdir(parents=True, exist_ok=True)
        args.answer.write_text(f"{rate:.2f}", encoding="utf-8")

    except (OSError, ValueError) as e:
        print(f"错误: {e}", file=sys.stderr)
        sys.exit(1)  # 优雅退出，状态码非0


if __name__ == "__main__":
    main()