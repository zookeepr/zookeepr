<%page args="parent" />
% if parent.contents() != '':
                            <div class="netv-block">
                                <div class="netv-block-tl"></div>
                                <div class="netv-block-tr"></div>
                                <div class="netv-block-bl"></div>
                                <div class="netv-block-br"></div>
                                <div class="netv-block-tc"></div>
                                <div class="netv-block-bc"></div>
                                <div class="netv-block-cl"></div>
                                <div class="netv-block-cr"></div>
                                <div class="netv-block-cc"></div>
                                <div class="netv-block-body">
                                    <div class="netv-blockheader">
                                        <div class="l"></div>
                                        <div class="r"></div>
                                        <div class="t">Contents</div>
                                    </div>
                                    <div class="netv-blockcontent">
                                        <div class="netv-blockcontent-body">
                                            <ul class="netv-vmenu">
                                                ${ parent.contents() | n }
                                            </ul>
                                            <div class="cleared"></div>
                                        </div>
                                    </div>
                                    <div class="cleared"></div>
                                </div>
                            </div>
 % endif
