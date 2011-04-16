${ h.latex_clean(c.text) | n }

<%
  layout = "" 
  for header in c.columns:
    layout += "l"
%>

\begin{tabular}{${ layout }}
${ " & ".join("\\bf %s" % f for f in c.columns) | n } \\\

% for row in c.data:
${ " & ".join(h.latex_clean(str(f)) for f in row) | n } \\\

% endfor

\end{tabular}

