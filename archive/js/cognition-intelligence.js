/**
 * Cognition Intelligence Module
 * Generates insights from cognitive telemetry data
 */

const CognitionIntelligence = {
  async loadData() {
    const response = await fetch('data/cognition-data.json?t=' + Date.now());
    return response.json();
  },

  // NOW tab insights
  generateNowInsights(data) {
    const { now } = data;
    
    return {
      headline: now.state,
      status: now.status,
      intervention: now.intervention,
      vitals: now.vitals,
      thoughtStream: now.thought_stream
    };
  },

  // MIND tab insights
  generateMindInsights(data) {
    const { mind } = data;
    
    // Find underused skills
    const underused = mind.skill_network.nodes.filter(n => n.status === 'underused' || n.status === 'neglected');
    
    // Calculate model routing efficiency
    const routingEfficiency = mind.model_routing.reduce((acc, r) => {
      acc.total += r.cost;
      acc.good += r.outcome === 'excellent' || r.outcome === 'good' ? 1 : 0;
      return acc;
    }, { total: 0, good: 0 });
    
    return {
      skills: mind.skill_network,
      underusedSkills: underused,
      routing: mind.model_routing,
      routingEfficiency: {
        cost: routingEfficiency.total.toFixed(2),
        qualityRate: Math.round((routingEfficiency.good / mind.model_routing.length) * 100)
      },
      decisions: mind.decision_quality,
      patterns: mind.thinking_patterns
    };
  },

  // MEMORY tab insights
  generateMemoryInsights(data) {
    const { memory } = data;
    
    // Identify at-risk lessons (not used recently)
    const atRisk = memory.long_term.lessons.filter(l => {
      const daysSince = Math.floor((Date.now() - new Date(l.last_used)) / (1000 * 60 * 60 * 24));
      return daysSince > 7;
    });
    
    return {
      working: memory.working,
      lessons: memory.long_term.lessons,
      atRiskLessons: atRisk,
      recall: memory.recall_performance
    };
  },

  // TRAINING tab insights
  generateTrainingInsights(data) {
    const { training } = data;
    
    // Separate blockers by owner
    const marcoBlockers = training.blockers.filter(b => b.action_required === 'Marco');
    const clawBlockers = training.blockers.filter(b => b.action_required === 'Claw');
    
    return {
      week: training.week,
      progress: training.progress,
      capabilities: training.capabilities_gained,
      marcoBlockers,
      clawBlockers,
      experiments: training.experiments,
      milestones: training.milestones
    };
  },

  // SYSTEM tab insights
  generateSystemInsights(data) {
    const { system } = data;
    
    // Identify stale files
    const staleFiles = Object.entries(system.core_files)
      .filter(([_, f]) => f.status === 'stale')
      .map(([name, _]) => name);
    
    // Calculate overall health
    const healthScores = Object.values(system.core_files).map(f => f.health);
    const overallHealth = Math.round(healthScores.reduce((a, b) => a + b, 0) / healthScores.length);
    
    return {
      files: system.core_files,
      staleFiles,
      overallHealth,
      environment: system.environmental_mastery,
      resources: system.resources,
      trading: system.trading_signal
    };
  },

  // Generate intervention if needed
  generateIntervention(data) {
    const { now, training } = data;
    
    const highPriorityBlockers = training.blockers.filter(b => b.priority === 'high');
    
    if (now.intervention.level === 'red' || highPriorityBlockers.length > 0) {
      return {
        show: true,
        level: now.intervention.level === 'red' ? 'red' : 'amber',
        message: now.intervention.message || highPriorityBlockers[0]?.title,
        action: now.intervention.action || highPriorityBlockers[0]?.description
      };
    }
    
    return { show: false };
  }
};

// Export
if (typeof module !== 'undefined') module.exports = CognitionIntelligence;
