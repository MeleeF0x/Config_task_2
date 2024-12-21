# MavenGraphViz

## What is it?
It is a cmd tool for visualizing a dependency graph. Dependencies are defined by the name of version control system git. The Graphvix representation is used to describe the dependency graph. The visualizer save the result inside the "output.dot" file in the form of a code.

## Flags
**cmd flags are set:**
- The path to the graph visualization program.
- The name of the commit being analyzed.
- The path to the result file in the form of a code.
- URL of the repository

## Example

```
python main.py --graphviz-path Graphviz\bin\dot.exe --repo-path git_repo --output-path output.dot
```
or
```
main.py --graphviz-path Graphviz\bin\dot.exe --repo-path git_repo --output-path output.dot
```
