\lcasection{Our Professional Delegates}
\begin{tabularx}{\textwidth+0.5cm}{l>{\raggedright\arraybackslash}X}<%
  companies = c.profs.keys()
  companies.sort()
%>
% for company in companies:
%   if company != '' and c.profs[company] is not None:
<%
      surnames = c.profs[company].keys()
      surnames.sort()
%>
%     for surname in surnames:
%       for name in c.profs[company][surname]:
${ h.latex_clean(name) | n } & ${ h.latex_clean(company) | n } \\\

%       endfor
%     endfor
%   endif
% endfor
% if "" in c.profs:
<%
    surnames = c.profs[""].keys()
    surnames.sort()
%>
%   for surname in surnames:
%     for name in c.profs[""][surname]:
${ h.latex_clean(name) | n } &  \\\

%     endfor
%   endfor
% endif
\end{tabularx}
