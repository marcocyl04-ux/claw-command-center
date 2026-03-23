        function renderMindTab() {
            const mind = cognitionData.mind || {};
            
            // Safety check
            if (!mind.skill_network || !mind.decisions) {
                console.error('MIND tab: Missing data', mind);
                return `
                    <div style="padding: var(--space-8); text-align: center; color: var(--danger);">
                        <div style="font-size: var(--text-2xl); margin-bottom: var(--space-4);">⚠ MIND Tab Error</div>
                        <div style="color: var(--text-secondary);">Missing cognitive data. Check console.</div>
                    </div>
                `;
            }
            
            // Render skill network after DOM update
            setTimeout(() => {
                if (mind.skill_network && mind.skill_network.nodes) {
                    renderSkillNetwork(mind.skill_network.nodes);
                }
            }, 0);
            
            return `
                <div class="state-hero">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <div class="state-headline">Cognitive Stack</div>
                            <div class="state-meta">How I process information and make decisions</div>
                        </div>
                        ${mind.decisions?.is_live ? `<span style="font-size: var(--text-xs); padding: var(--space-2) var(--space-3); background: rgba(74,222,128,0.1); border-radius: var(--radius-full); color: var(--success);">● Live</span>` : ''}
                    </div>
                </div>
                <div class="cards-grid">
                    <div class="card card-full">
                        <div class="section-header">
                            <span class="section-title">Skill Network</span>
                            <span style="font-size: var(--text-sm); color: var(--text-secondary);">${mind.skill_network?.nodes?.length || 22} skills installed • Click nodes to explore</span>
                        </div>
                        <div id="skillNetworkViz" style="height: 400px; background: var(--bg-1); border-radius: var(--radius-md); position: relative; overflow: hidden;">
                            <!-- SVG skill network will be rendered here -->
                        </div>
                        <div id="skillDetailPanel" style="display: none; margin-top: var(--space-4); background: var(--bg-1); border-radius: var(--radius-md); padding: var(--space-5); border-left: 3px solid var(--amber-500);">
                            <!-- Skill detail content -->
                        </div>
                    </div>
                    <div class="card card-full">
                        <div class="section-header">
                            <span class="section-title">Model Mastery</span>
                            <span style="font-size: var(--text-sm); color: var(--text-secondary);">6 models • Quality scores estimated • Costs from OpenRouter</span>
                        </div>
                        <div class="model-cards-grid">
                            ${getModelCardHTML('Opus 4.6', '~$0.10-0.50', 92, 'excellent', [
                                { task: 'Design systems', pct: 40 },
                                { task: 'Complex reasoning', pct: 30 },
                                { task: 'Architecture', pct: 20 }
                            ])}
                            ${getModelCardHTML('Sonnet 4.6', '~$0.02-0.08', 85, 'good', [
                                { task: 'Content generation', pct: 50 },
                                { task: 'Analysis', pct: 30 },
                                { task: 'Review', pct: 20 }
                            ])}
                            ${getModelCardHTML('Kimi K2.5', '~$0.001-0.005', 88, 'good', [
                                { task: 'Implementation', pct: 60 },
                                { task: 'Refactoring', pct: 25 },
                                { task: 'Debugging', pct: 15 }
                            ])}
                            ${getModelCardHTML('Qwen3 235B', '~$0.005-0.02', 82, 'good', [
                                { task: 'Analysis', pct: 45 },
                                { task: 'Bulk processing', pct: 35 },
                                { task: 'Market assessment', pct: 20 }
                            ])}
                            ${getModelCardHTML('DeepSeek R1', '~$0.001-0.005', 90, 'excellent', [
                                { task: 'Reasoning', pct: 50 },
                                { task: 'Self-review', pct: 30 },
                                { task: 'Meta-cognition', pct: 20 }
                            ])}
                            ${getModelCardHTML('Gemini 2.5 Pro', '~$0.01-0.05', 84, 'good', [
                                { task: 'Multimodal', pct: 40 },
                                { task: 'Long context', pct: 35 },
                                { task: 'Research', pct: 25 }
                            ])}
                        </div>
                        <div id="modelDetailPanel" style="display: none; margin-top: var(--space-5); background: var(--bg-1); border-radius: var(--radius-lg); padding: var(--space-5);">
                            <!-- Model detail content -->
                        </div>
                    </div>
                    <div class="card card-full">
                        <div class="section-header">
                            <span class="section-title">Decision Quality</span>
                            <span style="font-size: var(--text-sm); color: var(--text-secondary);">Trend: ${mind.decisions.trend} ${mind.decisions?.is_live ? '• Live' : ''}</span>
                        </div>
                        <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: var(--space-4); margin-bottom: var(--space-5);">
                            <div>
                                <div style="font-size: var(--text-sm); color: var(--text-tertiary); margin-bottom: var(--space-2);">Autonomous Decisions</div>
                                <div style="font-family: var(--font-mono); font-size: var(--text-2xl); font-weight: 700; color: var(--success);">${mind.decisions.autonomous.count}</div>
                                <div style="font-size: var(--text-sm); color: var(--text-secondary);">${mind.decisions.autonomous.quality}% quality</div>
                            </div>
                            <div>
                                <div style="font-size: var(--text-sm); color: var(--text-tertiary); margin-bottom: var(--space-2);">Escalated Decisions</div>
                                <div style="font-family: var(--font-mono); font-size: var(--text-2xl); font-weight: 700; color: var(--amber-400);">${mind.decisions.escalated.count}</div>
                                <div style="font-size: var(--text-sm); color: var(--text-secondary);">${mind.decisions.escalated.quality}% quality</div>
                            </div>
                        </div>
                        
                        <!-- Decision Stats Summary -->
                        <div style="background: var(--bg-1); border-radius: var(--radius-md); padding: var(--space-4); margin-bottom: var(--space-5);">
                            <div style="font-size: var(--text-sm); color: var(--text-tertiary); margin-bottom: var(--space-3);">Decision History</div>
                            <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: var(--space-4);">
                                <div style="text-align: center;">
                                    <div style="font-family: var(--font-mono); font-size: var(--text-2xl); font-weight: 700; color: var(--success);">${mind.decisions.examples?.length || 0}</div>
                                    <div style="font-size: var(--text-xs); color: var(--text-secondary);">Recent decisions tracked</div>
                                </div>
                                <div style="text-align: center;">
                                    <div style="font-family: var(--font-mono); font-size: var(--text-2xl); font-weight: 700; color: var(--amber-400);">${Math.round((mind.decisions.autonomous.count / (mind.decisions.autonomous.count + mind.decisions.escalated.count)) * 100) || 0}%</div>
                                    <div style="font-size: var(--text-xs); color: var(--text-secondary);">Autonomy rate</div>
                                </div>
                                <div style="text-align: center;">
                                    <div style="font-family: var(--font-mono); font-size: var(--text-2xl); font-weight: 700;">${mind.decisions.trend}</div>
                                    <div style="font-size: var(--text-xs); color: var(--text-secondary);">Current trend</div>
                                </div>
                            </div>
                        </div>
                        
                        <!-- Decision Pattern Note -->
                        <div style="background: var(--bg-1); border-radius: var(--radius-md); padding: var(--space-4); margin-bottom: var(--space-5); border-left: 3px solid var(--amber-500);">
                            <div style="font-size: var(--text-sm); color: var(--text-secondary);">
                                <strong>Note:</strong> Decision quality metrics are manually assessed. 
                                Autonomy rate calculated from recent session history.
                            </div>
                        </div>
                        
                        <div style="font-size: var(--text-sm); color: var(--text-tertiary); margin-bottom: var(--space-3); text-transform: uppercase; letter-spacing: 0.05em;">Recent Examples</div>
                        ${mind.decisions.examples.map(ex => `
                            <div style="background: var(--bg-1); border-radius: var(--radius-md); padding: var(--space-4); margin-bottom: var(--space-3); border-left: 3px solid ${ex.type === 'autonomous' ? 'var(--success)' : 'var(--amber-500)'};">
                                <div style="display: flex; justify-content: space-between; margin-bottom: var(--space-2);">
                                    <span style="font-weight: 600;">${ex.context}</span>
                                    <span style="font-size: var(--text-xs); text-transform: uppercase; color: ${ex.type === 'autonomous' ? 'var(--success)' : 'var(--amber-400)'};">${ex.type}</span>
                                </div>
                                <div style="color: var(--text-secondary); font-size: var(--text-sm); margin-bottom: var(--space-2);">
                                    <strong>Decision:</strong> ${ex.decision}
                                </div>
                                <div style="color: var(--text-tertiary); font-size: var(--text-sm); margin-bottom: var(--space-2);">
                                    <strong>Reasoning:</strong> ${ex.reasoning}
                                </div>
                                <div style="display: flex; justify-content: space-between; font-size: var(--text-xs); color: var(--text-tertiary);">
                                    <span>Outcome: ${ex.outcome}</span>
                                    <span>${ex.timestamp}</span>
                                </div>
                            </div>
                        `).join('')}
                    </div>
                    
                    <!-- Cognitive Load Monitor -->
                    <div class="card card-full">
                        <div class="section-header">
                            <span class="section-title">Cognitive Load</span>
                            <span style="font-size: var(--text-sm); color: var(--text-secondary);">Real-time system status</span>
                        </div>
                        
                        <!-- Context Window -->
                        <div style="margin-bottom: var(--space-5);">
                            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: var(--space-2);">
                                <span style="font-size: var(--text-sm); color: var(--text-secondary);">Context Window</span>
                                <span style="font-family: var(--font-mono); font-size: var(--text-sm);">47MB / 100MB</span>
                            </div>
                            <div style="height: 8px; background: var(--bg-1); border-radius: var(--radius-full); overflow: hidden; margin-bottom: var(--space-2);">
                                <div style="width: 47%; height: 100%; background: linear-gradient(to right, var(--success), var(--amber-500)); border-radius: var(--radius-full);"></div>
                            </div>
                            <div style="display: flex; align-items: center; gap: var(--space-2); font-size: var(--text-sm);">
                                <span style="color: var(--success);">● Healthy</span>
                                <span style="color: var(--text-tertiary);">— Within normal range</span>
                            </div>
                        </div>
                        
                        <!-- Active Threads -->
                        <div style="margin-bottom: var(--space-5);">
                            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: var(--space-2);">
                                <span style="font-size: var(--text-sm); color: var(--text-secondary);">Active Threads</span>
                                <span style="font-family: var(--font-mono); font-size: var(--text-sm);">3 parallel</span>
                            </div>
                            <div style="display: flex; gap: var(--space-2); margin-bottom: var(--space-2);">
                                <div style="padding: var(--space-2) var(--space-3); background: rgba(74,222,128,0.1); border-radius: var(--radius-md); font-size: var(--text-xs); color: var(--success);">Dashboard rebuild</div>
                                <div style="padding: var(--space-2) var(--space-3); background: rgba(74,222,128,0.1); border-radius: var(--radius-md); font-size: var(--text-xs); color: var(--success);">Skill network</div>
                                <div style="padding: var(--space-2) var(--space-3); background: rgba(74,222,128,0.1); border-radius: var(--radius-md); font-size: var(--text-xs); color: var(--success);">Model cards</div>
                            </div>
                            <div style="display: flex; align-items: center; gap: var(--space-2); font-size: var(--text-sm);">
                                <span style="color: var(--success);">● Manageable</span>
                                <span style="color: var(--text-tertiary);">— Processing normally</span>
                            </div>
                        </div>
                        
                        <!-- Attention Focus -->
                        <div style="margin-bottom: var(--space-5);">
                            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: var(--space-2);">
                                <span style="font-size: var(--text-sm); color: var(--text-secondary);">Attention Focus</span>
                                <span style="font-family: var(--font-mono); font-size: var(--text-sm);">87%</span>
                            </div>
                            <div style="height: 8px; background: var(--bg-1); border-radius: var(--radius-full); overflow: hidden; margin-bottom: var(--space-2);">
                                <div style="width: 87%; height: 100%; background: var(--amber-500); border-radius: var(--radius-full);"></div>
                            </div>
                            <div style="font-size: var(--text-sm); color: var(--text-secondary);">
                                Currently focused on: <strong>Dashboard MIND tab enhancements</strong>
                            </div>
                        </div>
                        
                        <!-- Intervention Panel (shown when needed) -->
                        <div style="background: linear-gradient(135deg, rgba(224,145,42,0.1) 0%, rgba(20,20,20,0.5) 100%); border: 1px solid rgba(224,145,42,0.3); border-radius: var(--radius-lg); padding: var(--space-5);">
                            <div style="display: flex; align-items: center; gap: var(--space-3); margin-bottom: var(--space-3);">
                                <div style="width: 40px; height: 40px; background: rgba(224,145,42,0.2); border-radius: var(--radius-md); display: flex; align-items: center; justify-content: center; font-size: var(--text-xl);">◈</div>
                                <div>
                                    <div style="font-weight: 600; color: var(--amber-400);">No Intervention Needed</div>
                                    <div style="font-size: var(--text-sm); color: var(--text-secondary);">All systems operating normally</div>
                                </div>
                            </div>
                            <div style="color: var(--text-secondary); font-size: var(--text-sm); margin-bottom: var(--space-3);">
                                When context window exceeds <strong>70%</strong> or active threads exceed <strong>5</strong>, intervention options will appear here.
                            </div>
