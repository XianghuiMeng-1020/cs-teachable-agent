import { useState, useMemo } from "react";
import { 
  Network, 
  Zap, 
  Target, 
  AlertCircle,
  Info,
  Maximize2,
  Minimize2,
  Filter
} from "lucide-react";
import { Card } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { cn } from "@/lib/utils";

interface KnowledgeUnit {
  id: string;
  name: string;
  prerequisites: string[];
  topic_group: string;
  learned: boolean;
  mastery_level: number; // 0-1
  dependent_count: number; // How many units depend on this
  difficulty: number; // 1-5
}

interface KnowledgeHeatmapProps {
  units: KnowledgeUnit[];
  className?: string;
}

export function KnowledgeHeatmap({ units, className }: KnowledgeHeatmapProps) {
  const [selectedUnit, setSelectedUnit] = useState<KnowledgeUnit | null>(null);
  const [viewMode, setViewMode] = useState<"dependencies" | "dependents">("dependencies");
  const [expanded, setExpanded] = useState(false);

  // Calculate matrix
  const matrix = useMemo(() => {
    const unitMap = new Map(units.map(u => [u.id, u]));
    const matrix: { from: string; to: string; strength: number; type: string }[] = [];

    units.forEach(unit => {
      // Prerequisites (incoming)
      unit.prerequisites.forEach(prereq => {
        const prereqUnit = unitMap.get(prereq);
        if (prereqUnit) {
          const strength = prereqUnit.mastery_level * (1 - unit.mastery_level);
          matrix.push({
            from: prereq,
            to: unit.id,
            strength,
            type: "prerequisite",
          });
        }
      });

      // Dependents (outgoing)
      const dependents = units.filter(u => u.prerequisites.includes(unit.id));
      dependents.forEach(dep => {
        const strength = unit.mastery_level * (1 - dep.mastery_level);
        matrix.push({
          from: unit.id,
          to: dep.id,
          strength,
          type: "dependent",
        });
      });
    });

    return matrix;
  }, [units]);

  // Get related units
  const getRelatedUnits = (unit: KnowledgeUnit) => {
    if (viewMode === "dependencies") {
      return unit.prerequisites
        .map(id => units.find(u => u.id === id))
        .filter(Boolean) as KnowledgeUnit[];
    } else {
      return units.filter(u => u.prerequisites.includes(unit.id));
    }
  };

  // Calculate heat colors
  const getHeatColor = (mastery: number) => {
    if (mastery >= 0.8) return "bg-emerald-500";
    if (mastery >= 0.6) return "bg-brand-500";
    if (mastery >= 0.4) return "bg-amber-500";
    if (mastery >= 0.2) return "bg-orange-500";
    return "bg-slate-300";
  };

  // Group by topic
  const groupedUnits = useMemo(() => {
    const groups: Record<string, KnowledgeUnit[]> = {};
    units.forEach(unit => {
      if (!groups[unit.topic_group]) {
        groups[unit.topic_group] = [];
      }
      groups[unit.topic_group].push(unit);
    });
    return groups;
  }, [units]);

  const topicColors: Record<string, string> = {
    variables_and_assignment: "bg-blue-100 text-blue-800",
    data_types: "bg-purple-100 text-purple-800",
    control_flow: "bg-amber-100 text-amber-800",
    functions: "bg-emerald-100 text-emerald-800",
    collections: "bg-rose-100 text-rose-800",
    default: "bg-slate-100 text-slate-800",
  };

  return (
    <Card padding="none" className={cn("overflow-hidden", className)}>
      {/* Header */}
      <div className="p-4 border-b border-slate-200 bg-slate-50">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-brand-100 rounded-lg">
              <Network className="w-5 h-5 text-brand-600" />
            </div>
            <div>
              <h3 className="font-semibold text-slate-900">Knowledge Dependency Heatmap</h3>
              <p className="text-sm text-slate-500">
                Visualize relationships and identify learning gaps
              </p>
            </div>
          </div>
          <div className="flex items-center gap-2">
            <Button
              variant="outline"
              size="sm"
              onClick={() => setExpanded(!expanded)}
              icon={expanded ? Minimize2 : Maximize2}
            >
              {expanded ? "Collapse" : "Expand"}
            </Button>
          </div>
        </div>

        {/* Legend */}
        <div className="flex items-center gap-4 mt-3 text-xs">
          <span className="text-slate-500">Mastery:</span>
          <div className="flex items-center gap-1">
            <div className="w-3 h-3 bg-slate-300 rounded" />
            <span>0-20%</span>
          </div>
          <div className="flex items-center gap-1">
            <div className="w-3 h-3 bg-orange-500 rounded" />
            <span>20-40%</span>
          </div>
          <div className="flex items-center gap-1">
            <div className="w-3 h-3 bg-amber-500 rounded" />
            <span>40-60%</span>
          </div>
          <div className="flex items-center gap-1">
            <div className="w-3 h-3 bg-brand-500 rounded" />
            <span>60-80%</span>
          </div>
          <div className="flex items-center gap-1">
            <div className="w-3 h-3 bg-emerald-500 rounded" />
            <span>80-100%</span>
          </div>
        </div>
      </div>

      <div className={cn("grid", expanded ? "grid-cols-1 lg:grid-cols-3" : "grid-cols-1")}>
        {/* Heatmap Grid */}
        <div className={cn("p-4", expanded ? "lg:col-span-2" : "")}>
          <div className="space-y-4">
            {Object.entries(groupedUnits).map(([topic, topicUnits]) => (
              <div key={topic}>
                <div className={cn(
                  "inline-flex items-center gap-2 px-3 py-1 rounded-full text-xs font-medium mb-2",
                  topicColors[topic] || topicColors.default
                )}>
                  <span className="capitalize">{topic.replace(/_/g, " ")}</span>
                  <span className="opacity-60">({topicUnits.length})</span>
                </div>
                
                <div className="grid grid-cols-4 sm:grid-cols-6 md:grid-cols-8 gap-2">
                  {topicUnits.map(unit => (
                    <button
                      key={unit.id}
                      onClick={() => setSelectedUnit(unit)}
                      className={cn(
                        "relative h-12 rounded-lg transition-all hover:scale-105",
                        getHeatColor(unit.mastery_level),
                        selectedUnit?.id === unit.id && "ring-2 ring-slate-900 ring-offset-2"
                      )}
                      title={`${unit.name}\nMastery: ${Math.round(unit.mastery_level * 100)}%\nDifficulty: ${unit.difficulty}/5`}
                    >
                      {/* Difficulty indicator */}
                      <div className="absolute top-1 right-1 w-1.5 h-1.5 rounded-full bg-white/50" />
                      
                      {/* Prerequisites indicator */}
                      {unit.prerequisites.length > 0 && (
                        <div className="absolute bottom-1 left-1 flex -space-x-0.5">
                          {unit.prerequisites.slice(0, 3).map((_, i) => (
                            <div
                              key={i}
                              className="w-1 h-1 rounded-full bg-white/40"
                            />
                          ))}
                        </div>
                      )}
                    </button>
                  ))}
                </div>
              </div>
            ))}
          </div>

          {/* Connection visualization */}
          {selectedUnit && (
            <div className="mt-6 p-4 bg-slate-50 rounded-xl">
              <div className="flex items-center justify-between mb-3">
                <h4 className="font-medium text-slate-900 flex items-center gap-2">
                  <Zap className="w-4 h-4 text-amber-500" />
                  Dependencies for {selectedUnit.name}
                </h4>
                <div className="flex gap-2">
                  <button
                    onClick={() => setViewMode("dependencies")}
                    className={cn(
                      "px-3 py-1 rounded-full text-xs font-medium transition-colors",
                      viewMode === "dependencies"
                        ? "bg-brand-500 text-white"
                        : "bg-slate-200 text-slate-600"
                    )}
                  >
                    Prerequisites
                  </button>
                  <button
                    onClick={() => setViewMode("dependents")}
                    className={cn(
                      "px-3 py-1 rounded-full text-xs font-medium transition-colors",
                      viewMode === "dependents"
                        ? "bg-brand-500 text-white"
                        : "bg-slate-200 text-slate-600"
                    )}
                  >
                    Dependents
                  </button>
                </div>
              </div>

              <div className="flex flex-wrap gap-2">
                {getRelatedUnits(selectedUnit).map(related => {
                  const isBlocked = viewMode === "dependents" && 
                    selectedUnit.mastery_level < 0.6;
                  
                  return (
                    <div
                      key={related.id}
                      className={cn(
                        "flex items-center gap-2 px-3 py-2 rounded-lg border",
                        getHeatColor(related.mastery_level),
                        isBlocked ? "opacity-50" : "opacity-100"
                      )}
                    >
                      <span className="text-sm font-medium text-white">
                        {related.name}
                      </span>
                      <span className="text-xs text-white/80">
                        {Math.round(related.mastery_level * 100)}%
                      </span>
                    </div>
                  );
                })}
                
                {getRelatedUnits(selectedUnit).length === 0 && (
                  <p className="text-sm text-slate-500">
                    No {viewMode === "dependencies" ? "prerequisites" : "dependents"} found
                  </p>
                )}
              </div>

              {viewMode === "dependents" && selectedUnit.mastery_level < 0.6 && (
                <div className="mt-3 flex items-center gap-2 text-sm text-amber-700 bg-amber-50 p-2 rounded-lg">
                  <AlertCircle className="w-4 h-4" />
                  <span>Learn this concept better to unlock dependent topics</span>
                </div>
              )}
            </div>
          )}
        </div>

        {/* Sidebar - Stats */}
        {expanded && (
          <div className="border-l border-slate-200 p-4 bg-slate-50">
            <h4 className="font-medium text-slate-900 mb-4 flex items-center gap-2">
              <Target className="w-4 h-4" />
              Network Statistics
            </h4>

            <div className="space-y-4">
              <div className="p-3 bg-white rounded-lg">
                <p className="text-sm text-slate-500">Total Concepts</p>
                <p className="text-2xl font-bold text-slate-900">{units.length}</p>
              </div>

              <div className="p-3 bg-white rounded-lg">
                <p className="text-sm text-slate-500">Learned</p>
                <p className="text-2xl font-bold text-emerald-600">
                  {units.filter(u => u.learned).length}
                </p>
              </div>

              <div className="p-3 bg-white rounded-lg">
                <p className="text-sm text-slate-500">Average Mastery</p>
                <p className="text-2xl font-bold text-brand-600">
                  {Math.round(units.reduce((a, b) => a + b.mastery_level, 0) / units.length * 100)}%
                </p>
              </div>

              <div className="p-3 bg-white rounded-lg">
                <p className="text-sm text-slate-500">Critical Path Length</p>
                <p className="text-2xl font-bold text-amber-600">
                  {Math.max(...units.map(u => u.prerequisites.length)) + 1}
                </p>
              </div>

              {/* Dependency counts */}
              <div>
                <p className="text-sm font-medium text-slate-700 mb-2">Dependencies per Unit</p>
                <div className="space-y-1">
                  {[0, 1, 2, 3].map(count => {
                    const matching = units.filter(u => u.prerequisites.length === count).length;
                    if (matching === 0) return null;
                    
                    return (
                      <div key={count} className="flex items-center gap-2 text-sm">
                        <div className="w-16 text-slate-500">{count} deps</div>
                        <div className="flex-1 h-2 bg-slate-200 rounded-full overflow-hidden">
                          <div
                            className="h-full bg-brand-500 rounded-full"
                            style={{ width: `${(matching / units.length) * 100}%` }}
                          />
                        </div>
                        <div className="w-8 text-right text-slate-600">{matching}</div>
                      </div>
                    );
                  })}
                </div>
              </div>

              {/* Bottlenecks */}
              <div className="p-3 bg-amber-50 rounded-lg border border-amber-200">
                <div className="flex items-center gap-2 text-amber-800">
                  <AlertCircle className="w-4 h-4" />
                  <span className="font-medium">Learning Bottlenecks</span>
                </div>
                <p className="text-sm text-amber-700 mt-2">
                  {units.filter(u => u.mastery_level < 0.4 && u.dependent_count > 2).length} concepts 
                  have low mastery but many dependents
                </p>
              </div>
            </div>
          </div>
        )}
      </div>
    </Card>
  );
}
