function renderMindTab() {
    const mind = cognitionData.mind || {};
    
    // Safety check
    if (!mind.skill_network || !mind.decisions) {
        console.error('MIND tab: Missing data', mind);
        return `
            <div class="p-12 text-center">
                <div class="font-headline text-2xl mb-4 text-primary-container">MIND Tab Error</div>
                <div class="text-on-surface/60">Missing cognitive data. Check console.</div>
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
        <!-- Header -->
        <div class="flex flex-col sm:flex-row sm:justify-between sm:items-end gap-4 mb-12">
            <div>
                <h1 class="font-headline text-4xl sm:text-5xl italic tracking-tight mb-2 text-on-surface">Cognitive Stack</h1>
                <p class="text-on-surface-variant/60 font-body text-sm uppercase tracking-widest">How I process information and make decisions</p>
            </div>
            ${mind.decisions?.is_live ? `
            <div class="flex items-center gap-2 px-3 py-1.5 bg-surface-container-low hairline-border rounded">
                <span class="w-1.5 h-1.5 rounded-full bg-tertiary animate-pulse"></span>
                <span class="text-[11px] font-mono uppercase tracking-wider text-tertiary">Live</span>
            </div>` : ''}
        </div>
        
        <!-- Bento Grid -->
        <div class="grid grid-cols-1 lg:grid-cols-12 gap-6">
            <!-- Skill Network (8 cols) -->
            <div class="lg:col-span-8">
                <div class="milled-surface hairline-border rounded p-6 h-[500px]">
                    <div class="flex justify-between items-center mb-6">
                        <h3 class="font-headline text-xl italic">Skill Network</h3>
                        <span class="text-[10px] font-mono text-on-surface/40 uppercase tracking-widest">${mind.skill_network?.nodes?.length || 22} Skills</span>
                    </div>
                    <div id="skillNetworkViz" class="h-[380px] bg-surface-container-low rounded relative overflow-hidden"></div>
                    <div id="skillDetailPanel" class="hidden mt-4 p-5 bg-surface-container-low rounded border-l-2 border-primary-container"></div>
                </div>
            </div>
            
            <!-- Decision Stats (4 cols) -->
            <div class="lg:col-span-4 flex flex-col gap-6">
                <div class="milled-surface hairline-border rounded p-6">
                    <h3 class="font-headline text-xl italic mb-8">Decision Quality</h3>
                    <div class="space-y-8">
                        <div>
                            <div class="flex justify-between items-end mb-2">
                                <span class="text-[10px] font-mono uppercase tracking-widest text-on-surface/40">Autonomous</span>
                                <span class="text-sm font-mono text-tertiary">${mind.decisions.autonomous.count}</span>
                            </div>
                            <div class="h-px w-full bg-outline-variant/20 relative">
                                <div class="absolute top-0 left-0 h-px bg-tertiary" style="width: ${mind.decisions.autonomous.quality}%"></div>
                            </div>
                            <div class="text-[10px] font-mono text-on-surface/40 mt-1">${mind.decisions.autonomous.quality}% quality</div>
                        </div>
                        <div>
                            <div class="flex justify-between items-end mb-2">
                                <span class="text-[10px] font-mono uppercase tracking-widest text-on-surface/40">Escalated</span>
                                <span class="text-sm font-mono text-primary-container">${mind.decisions.escalated.count}</span>
                            </div>
                            <div class="h-px w-full bg-outline-variant/20 relative">
                                <div class="absolute top-0 left-0 h-px bg-primary-container" style="width: ${mind.decisions.escalated.quality}%"></div>
                            </div>
                            <div class="text-[10px] font-mono text-on-surface/40 mt-1">${mind.decisions.escalated.quality}% quality</div>
                        </div>
                    </div>
                </div>
                
                <div class="milled-surface hairline-border rounded p-6">
                    <h3 class="font-headline text-xl italic mb-2">Autonomy Rate</h3>
                    <div class="font-mono text-4xl text-primary-container mb-2">${Math.round((mind.decisions.autonomous.count / (mind.decisions.autonomous.count + mind.decisions.escalated.count)) * 100) || 0}%</div>
                    <p class="text-[10px] font-mono text-on-surface/40 uppercase tracking-widest">Trend: ${mind.decisions.trend}</p>
                </div>
            </div>
            
            <!-- Model Mastery (Full width) -->
            <div class="lg:col-span-12">
                <div class="milled-surface hairline-border rounded p-6">
                    <div class="flex justify-between items-center mb-6">
                        <h3 class="font-headline text-xl italic">Model Mastery</h3>
                        <span class="text-[10px] font-mono text-on-surface/40 uppercase tracking-widest">6 Models • OpenRouter</span>
                    </div>
                    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
                        ${getModelCardHTML('Opus 4.6', '~$0.10-0.50', 92, [{ task: 'Design', pct: 40 }, { task: 'Reasoning', pct: 30 }, { task: 'Architecture', pct: 20 }])}
                        ${getModelCardHTML('Sonnet 4.6', '~$0.02-0.08', 85, [{ task: 'Content', pct: 50 }, { task: 'Analysis', pct: 30 }, { task: 'Review', pct: 20 }])}
                        ${getModelCardHTML('Kimi K2.5', '~$0.001-0.005', 88, [{ task: 'Impl', pct: 60 }, { task: 'Refactor', pct: 25 }, { task: 'Debug', pct: 15 }])}
                        ${getModelCardHTML('Qwen3 235B', '~$0.005-0.02', 82, [{ task: 'Analysis', pct: 45 }, { task: 'Bulk', pct: 35 }, { task: 'Market', pct: 20 }])}
                        ${getModelCardHTML('DeepSeek R1', '~$0.001-0.005', 90, [{ task: 'Reasoning', pct: 50 }, { task: 'Review', pct: 30 }, { task: 'Meta', pct: 20 }])}
                        ${getModelCardHTML('Gemini 2.5', '~$0.01-0.05', 84, [{ task: 'Multi', pct: 40 }, { task: 'Context', pct: 35 }, { task: 'Research', pct: 25 }])}
                    </div>
                    <div id="modelDetailPanel" class="hidden mt-6 p-5 bg-surface-container-low rounded"></div>
                </div>
            </div>
        </div>
    `;
}