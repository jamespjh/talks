// gvpr program: light up the nodes and edges whose "role" is ARGV[0], dim the rest.
// The harness stays bright throughout so every slide shows what the piece plugs into.
// With no argument (or "all") the graph is passed through unchanged.
// Usage: gvpr -c -a <role> -f highlight.g agent.dot | dot -Tsvg
BEGIN { string want = (ARGC > 0) ? ARGV[0] : "all"; }
N {
    if (want == "all") { }
    else if ($.role == want) { fillcolor = "#a433ff"; fontcolor = "#f5f5f5"; color = "#f5f5f5"; penwidth = "4"; }
    else if ($.role == "harness") { }
    else { fillcolor = "#5b3a78"; fontcolor = "#9c88ad"; color = "#5b3a78"; }
}
E {
    if (want == "all") { }
    else if ($.role == want) { color = "#f5f5f5"; penwidth = "4"; }
    else { color = "#5b3a78"; fontcolor = "#7a6090"; }
}
