import os
import subprocess
import argparse
import tempfile
from pathlib import Path

def get_git_commit_dependencies(repo_path):
    os.chdir(repo_path)
    result = subprocess.run(["git", "log", "--name-only", "--pretty=format:%H"], capture_output=True, text=True)

    if result.returncode != 0:
        raise RuntimeError(f"Git command failed: {result.stderr}")

    lines = result.stdout.splitlines()
    dependencies = {}
    current_commit = None

    for line in lines:
        if line.strip():
            if len(line.strip()) == 40 and not line.strip().startswith(' '):  # Likely a commit hash
                current_commit = line.strip()
                dependencies[current_commit] = set()
            elif current_commit:
                dependencies[current_commit].add(line.strip())

    return dependencies

def generate_graphviz_code(dependencies):
    dot = ["digraph G {"]

    for commit, items in dependencies.items():
        commit_node = f'"{commit}"'
        dot.append(f"    {commit_node} [shape=box, style=filled, color=lightblue]")

        for item in items:
            item_node = f'"{item}"'
            dot.append(f"    {item_node} [shape=ellipse]")
            dot.append(f"    {commit_node} -> {item_node}")

    dot.append("}")
    return "\n".join(dot)

def save_graph_to_file(graph_code, output_path):
    with open(output_path, 'w') as file:
        file.write(graph_code)


def main():
    parser = argparse.ArgumentParser(description="Visualize Git repository dependencies using Graphviz.")
    parser.add_argument("--graphviz-path", required=True, help="Path to Graphviz tool (e.g., dot)")
    parser.add_argument("--repo-path", required=True, help="Path to the Git repository")
    parser.add_argument("--output-path", required=True, help="Path to the output file for Graphviz code")

    args = parser.parse_args()

    try:
        dependencies = get_git_commit_dependencies(args.repo_path)
        graph_code = generate_graphviz_code(dependencies)
        save_graph_to_file(graph_code, args.output_path)

        print("Graphviz code saved to", args.output_path)
        print("Run the following command to visualize:")
        print(f"{args.graphviz_path} -Tpng {args.output_path} -o output.png")

    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    main()

#main.py --graphviz-path Graphviz\bin\dot.exe --repo-path git_repo --output-path output.dot
#python main.py --graphviz-path Graphviz\bin\dot.exe --repo-path git_repo --output-path output.dot