// A/B Testing and Experimentation Framework
// Supports feature flags, A/B tests, and gradual rollouts

import { useState, useEffect, useCallback, useContext, createContext } from 'react';

interface Experiment {
  id: string;
  name: string;
  description?: string;
  variants: ExperimentVariant[];
  trafficAllocation?: number; // 0-100, percentage of users in experiment
}

interface ExperimentVariant {
  id: string;
  name: string;
  weight: number; // 0-100, relative weight within experiment
  payload?: Record<string, any>;
}

interface ExperimentAssignment {
  experimentId: string;
  variantId: string;
  payload?: Record<string, any>;
  timestamp: string;
}

// Experiment storage key
const EXPERIMENT_STORAGE_KEY = 'cs_ta_experiments';
const USER_ID_KEY = 'cs_ta_user_id';

// Generate consistent user ID
function getOrCreateUserId(): string {
  let userId = localStorage.getItem(USER_ID_KEY);
  if (!userId) {
    userId = `user_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    localStorage.setItem(USER_ID_KEY, userId);
  }
  return userId;
}

// Hash function for consistent assignment
function hashString(str: string): number {
  let hash = 0;
  for (let i = 0; i < str.length; i++) {
    const char = str.charCodeAt(i);
    hash = ((hash << 5) - hash) + char;
    hash = hash & hash; // Convert to 32bit integer
  }
  return Math.abs(hash);
}

// Get variant assignment based on user ID
function assignVariant(experiment: Experiment, userId: string): ExperimentVariant {
  const hash = hashString(`${experiment.id}_${userId}`);
  const totalWeight = experiment.variants.reduce((sum, v) => sum + v.weight, 0);
  const normalizedHash = hash % totalWeight;
  
  let cumulativeWeight = 0;
  for (const variant of experiment.variants) {
    cumulativeWeight += variant.weight;
    if (normalizedHash < cumulativeWeight) {
      return variant;
    }
  }
  
  return experiment.variants[0]; // Fallback
}

// Experiment Manager
class ExperimentManager {
  private experiments: Map<string, Experiment> = new Map();
  private assignments: Map<string, ExperimentAssignment> = new Map();
  private userId: string;
  private listeners: Set<(assignments: Map<string, ExperimentAssignment>) => void> = new Set();

  constructor() {
    this.userId = getOrCreateUserId();
    this.loadAssignments();
  }

  // Register an experiment
  registerExperiment(experiment: Experiment) {
    this.experiments.set(experiment.id, experiment);
    
    // Auto-assign if not already assigned
    if (!this.assignments.has(experiment.id)) {
      this.assignUser(experiment.id);
    }
  }

  // Assign user to experiment variant
  private assignUser(experimentId: string): ExperimentAssignment | null {
    const experiment = this.experiments.get(experimentId);
    if (!experiment) return null;

    // Check traffic allocation
    const trafficHash = hashString(`${experimentId}_traffic_${this.userId}`);
    if ((trafficHash % 100) >= (experiment.trafficAllocation || 100)) {
      return null; // User not in experiment
    }

    const variant = assignVariant(experiment, this.userId);
    const assignment: ExperimentAssignment = {
      experimentId,
      variantId: variant.id,
      payload: variant.payload,
      timestamp: new Date().toISOString(),
    };

    this.assignments.set(experimentId, assignment);
    this.saveAssignments();
    this.notifyListeners();

    // Log assignment (could send to analytics)
    console.log('[Experiment] Assigned:', { experimentId, variantId: variant.id, userId: this.userId });

    return assignment;
  }

  // Get variant for an experiment
  getVariant(experimentId: string): ExperimentVariant | null {
    // Check if already assigned
    const assignment = this.assignments.get(experimentId);
    if (assignment) {
      const experiment = this.experiments.get(experimentId);
      return experiment?.variants.find(v => v.id === assignment.variantId) || null;
    }

    // Try to assign
    this.assignUser(experimentId);
    const newAssignment = this.assignments.get(experimentId);
    if (newAssignment) {
      const experiment = this.experiments.get(experimentId);
      return experiment?.variants.find(v => v.id === newAssignment.variantId) || null;
    }

    return null;
  }

  // Get assignment payload
  getPayload(experimentId: string): Record<string, any> | undefined {
    const assignment = this.assignments.get(experimentId);
    return assignment?.payload;
  }

  // Check if user is in specific variant
  isInVariant(experimentId: string, variantId: string): boolean {
    const assignment = this.assignments.get(experimentId);
    return assignment?.variantId === variantId;
  }

  // Check if feature is enabled (for feature flags)
  isEnabled(experimentId: string): boolean {
    return this.assignments.has(experimentId);
  }

  // Force variant assignment (for testing)
  forceVariant(experimentId: string, variantId: string) {
    const experiment = this.experiments.get(experimentId);
    const variant = experiment?.variants.find(v => v.id === variantId);
    
    if (variant) {
      const assignment: ExperimentAssignment = {
        experimentId,
        variantId,
        payload: variant.payload,
        timestamp: new Date().toISOString(),
      };
      this.assignments.set(experimentId, assignment);
      this.saveAssignments();
      this.notifyListeners();
    }
  }

  // Track experiment event
  trackEvent(experimentId: string, eventName: string, properties?: Record<string, any>) {
    const assignment = this.assignments.get(experimentId);
    if (!assignment) return;

    const event = {
      experimentId,
      variantId: assignment.variantId,
      eventName,
      properties,
      timestamp: new Date().toISOString(),
      userId: this.userId,
    };

    // Send to analytics
    console.log('[Experiment] Event:', event);
    
    // Could also send to your analytics service:
    // analytics.track(`Experiment: ${experimentId}`, event);
  }

  // Get all assignments
  getAllAssignments(): ExperimentAssignment[] {
    return Array.from(this.assignments.values());
  }

  // Subscribe to changes
  subscribe(listener: (assignments: Map<string, ExperimentAssignment>) => void) {
    this.listeners.add(listener);
    return () => this.listeners.delete(listener);
  }

  private notifyListeners() {
    this.listeners.forEach(listener => listener(this.assignments));
  }

  // Persist assignments
  private saveAssignments() {
    const data = JSON.stringify(Array.from(this.assignments.entries()));
    localStorage.setItem(EXPERIMENT_STORAGE_KEY, data);
  }

  private loadAssignments() {
    try {
      const data = localStorage.getItem(EXPERIMENT_STORAGE_KEY);
      if (data) {
        const entries = JSON.parse(data) as [string, ExperimentAssignment][];
        this.assignments = new Map(entries);
      }
    } catch (e) {
      console.error('[Experiment] Failed to load assignments:', e);
    }
  }

  // Reset all assignments (for testing)
  reset() {
    this.assignments.clear();
    this.saveAssignments();
    this.notifyListeners();
  }
}

// Singleton instance
const experimentManager = new ExperimentManager();

// React Context for experiments
interface ExperimentContextValue {
  getVariant: (experimentId: string) => ExperimentVariant | null;
  getPayload: (experimentId: string) => Record<string, any> | undefined;
  isInVariant: (experimentId: string, variantId: string) => boolean;
  isEnabled: (experimentId: string) => boolean;
  trackEvent: (experimentId: string, eventName: string, properties?: Record<string, any>) => void;
  forceVariant: (experimentId: string, variantId: string) => void;
}

const ExperimentContext = createContext<ExperimentContextValue | null>(null);

// Provider component
export function ExperimentProvider({ 
  children, 
  experiments 
}: { 
  children: React.ReactNode;
  experiments: Experiment[];
}) {
  useEffect(() => {
    // Register all experiments
    experiments.forEach(exp => experimentManager.registerExperiment(exp));
  }, [experiments]);

  const value: ExperimentContextValue = {
    getVariant: (id) => experimentManager.getVariant(id),
    getPayload: (id) => experimentManager.getPayload(id),
    isInVariant: (id, variant) => experimentManager.isInVariant(id, variant),
    isEnabled: (id) => experimentManager.isEnabled(id),
    trackEvent: (id, event, props) => experimentManager.trackEvent(id, event, props),
    forceVariant: (id, variant) => experimentManager.forceVariant(id, variant),
  };

  return (
    <ExperimentContext.Provider value={value}>
      {children}
    </ExperimentContext.Provider>
  );
}

// Hook for using experiments
export function useExperiment(experimentId: string) {
  const context = useContext(ExperimentContext);
  if (!context) {
    throw new Error('useExperiment must be used within ExperimentProvider');
  }

  const [variant, setVariant] = useState(() => context.getVariant(experimentId));

  useEffect(() => {
    const unsubscribe = experimentManager.subscribe(() => {
      setVariant(context.getVariant(experimentId));
    });
    return unsubscribe;
  }, [experimentId, context]);

  const trackEvent = useCallback(
    (eventName: string, properties?: Record<string, any>) => {
      context.trackEvent(experimentId, eventName, properties);
    },
    [experimentId, context]
  );

  return {
    variant,
    payload: context.getPayload(experimentId),
    isInVariant: (variantId: string) => context.isInVariant(experimentId, variantId),
    isEnabled: context.isEnabled(experimentId),
    trackEvent,
  };
}

// Hook for feature flags
export function useFeatureFlag(flagId: string): boolean {
  const context = useContext(ExperimentContext);
  if (!context) {
    throw new Error('useFeatureFlag must be used within ExperimentProvider');
  }

  const [enabled, setEnabled] = useState(() => context.isEnabled(flagId));

  useEffect(() => {
    const unsubscribe = experimentManager.subscribe(() => {
      setEnabled(context.isEnabled(flagId));
    });
    return unsubscribe;
  }, [flagId, context]);

  return enabled;
}

// Predefined experiments
export const DEFAULT_EXPERIMENTS: Experiment[] = [
  {
    id: 'onboarding_v2',
    name: 'New Onboarding Flow',
    description: 'Test new interactive onboarding vs. static guide',
    variants: [
      { id: 'control', name: 'Current Guide', weight: 50 },
      { id: 'interactive', name: 'Interactive Tour', weight: 50, payload: { showTooltips: true } },
    ],
    trafficAllocation: 100,
  },
  {
    id: 'teaching_hints',
    name: 'Teaching Helper Hints',
    description: 'Test frequency of teaching quality hints',
    variants: [
      { id: 'always', name: 'Always Show', weight: 33, payload: { frequency: 'always' } },
      { id: 'sometimes', name: 'Sometimes', weight: 33, payload: { frequency: 'sometimes' } },
      { id: 'rarely', name: 'Rarely', weight: 34, payload: { frequency: 'rarely' } },
    ],
    trafficAllocation: 100,
  },
  {
    id: 'achievement_notifications',
    name: 'Achievement Notification Style',
    description: 'Test different achievement notification styles',
    variants: [
      { id: 'toast', name: 'Toast', weight: 50 },
      { id: 'modal', name: 'Modal', weight: 50, payload: { useModal: true } },
    ],
    trafficAllocation: 50,
  },
];

// Export singleton for direct use
export { experimentManager };
