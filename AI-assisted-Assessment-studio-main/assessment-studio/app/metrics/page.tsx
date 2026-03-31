import Link from "next/link";
import ArrowForwardRounded from "@mui/icons-material/ArrowForwardRounded";
import AssessmentRounded from "@mui/icons-material/AssessmentRounded";
import AutoGraphRounded from "@mui/icons-material/AutoGraphRounded";
import BoltRounded from "@mui/icons-material/BoltRounded";
import InsightsRounded from "@mui/icons-material/InsightsRounded";
import NorthEastRounded from "@mui/icons-material/NorthEastRounded";
import PsychologyAltRounded from "@mui/icons-material/PsychologyAltRounded";
import QueryStatsRounded from "@mui/icons-material/QueryStatsRounded";
import ShieldRounded from "@mui/icons-material/ShieldRounded";
import { alpha, Box, Button, Chip, Paper, Stack, Typography } from "@mui/material";
import { getMetricsDashboardData, type MetricsDashboardData } from "@/src/server/metrics-data";

export const metadata = {
  title: "Learning Analytics Dashboard",
  description: "Assessment Studio analytics dashboard for typed items, AI pass rates, and student telemetry."
};

const chartColors = {
  ink: "#17212B",
  muted: "#60707F",
  border: "#E3E8EE",
  parsons: "#4F73B8",
  dropdown: "#D6656A",
  execution: "#4FBF85",
  success: "#46705C",
  warning: "#8D6A34",
  danger: "#A14740",
  primary: "#1E6676"
};

function formatPercent(value: number | null): string {
  if (value === null || Number.isNaN(value)) {
    return "—";
  }
  return `${value.toFixed(1)}%`;
}

function formatCompactNumber(value: number): string {
  if (value >= 1000) {
    return Intl.NumberFormat("en", {
      notation: "compact",
      maximumFractionDigits: 1
    }).format(value);
  }
  return String(value);
}

function formatDateTime(value: string): string {
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) {
    return "—";
  }
  return new Intl.DateTimeFormat("en", {
    month: "short",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit"
  }).format(date);
}

function formatDuration(value: number | null): string {
  if (value === null || Number.isNaN(value)) {
    return "—";
  }
  const seconds = Math.round(value / 1000);
  if (seconds < 60) {
    return `${seconds}s`;
  }
  const minutes = Math.floor(seconds / 60);
  const remainder = seconds % 60;
  return `${minutes}m ${remainder}s`;
}

function itemTypeLabel(itemType: string): string {
  if (itemType === "execution-trace") {
    return "Execution trace";
  }
  return itemType.charAt(0).toUpperCase() + itemType.slice(1);
}

function passTone(passRate: number | null): { bg: string; fg: string; border: string } {
  if (passRate === null) {
    return {
      bg: alpha(chartColors.muted, 0.08),
      fg: chartColors.muted,
      border: alpha(chartColors.muted, 0.14)
    };
  }
  if (passRate <= 25) {
    return {
      bg: alpha(chartColors.success, 0.12),
      fg: chartColors.success,
      border: alpha(chartColors.success, 0.18)
    };
  }
  if (passRate <= 75) {
    return {
      bg: alpha(chartColors.warning, 0.12),
      fg: chartColors.warning,
      border: alpha(chartColors.warning, 0.18)
    };
  }
  return {
    bg: alpha(chartColors.danger, 0.12),
    fg: chartColors.danger,
    border: alpha(chartColors.danger, 0.18)
  };
}

function positiveTone(ratio: number | null): { bg: string; fg: string; border: string } {
  if (ratio === null) {
    return {
      bg: alpha(chartColors.muted, 0.08),
      fg: chartColors.muted,
      border: alpha(chartColors.muted, 0.14)
    };
  }
  if (ratio >= 80) {
    return {
      bg: alpha(chartColors.success, 0.12),
      fg: chartColors.success,
      border: alpha(chartColors.success, 0.18)
    };
  }
  if (ratio >= 50) {
    return {
      bg: alpha(chartColors.primary, 0.12),
      fg: chartColors.primary,
      border: alpha(chartColors.primary, 0.18)
    };
  }
  return {
    bg: alpha(chartColors.warning, 0.12),
    fg: chartColors.warning,
    border: alpha(chartColors.warning, 0.18)
  };
}

function countBarWidth(value: number, maxValue: number): number {
  if (maxValue <= 0) {
    return 0;
  }
  return (value / maxValue) * 100;
}

function SectionFrame({
  eyebrow,
  title,
  action,
  children
}: {
  eyebrow?: string;
  title: string;
  action?: React.ReactNode;
  children: React.ReactNode;
}) {
  return (
    <Paper
      sx={{
        p: { xs: 2.25, md: 2.75 },
        borderRadius: 4,
        position: "relative",
        overflow: "hidden",
        "&::before": {
          content: '""',
          position: "absolute",
          inset: "0 0 auto 0",
          height: 3,
          background: `linear-gradient(90deg, ${alpha(chartColors.primary, 0.9)} 0%, ${alpha(chartColors.execution, 0.55)} 100%)`
        }
      }}
    >
      <Stack spacing={2}>
        <Stack
          direction={{ xs: "column", sm: "row" }}
          justifyContent="space-between"
          alignItems={{ xs: "flex-start", sm: "center" }}
          spacing={1.25}
        >
          <Stack spacing={0.35}>
            {eyebrow ? (
              <Typography variant="caption" sx={{ textTransform: "uppercase", letterSpacing: "0.08em" }}>
                {eyebrow}
              </Typography>
            ) : null}
            <Typography variant="h2">{title}</Typography>
          </Stack>
          {action}
        </Stack>
        {children}
      </Stack>
    </Paper>
  );
}

function StatCard({
  label,
  value,
  icon,
  helper
}: {
  label: string;
  value: string;
  icon: React.ReactNode;
  helper?: string;
}) {
  return (
    <Paper
      sx={{
        p: 2.1,
        borderRadius: 3.5,
        boxShadow: "none",
        bgcolor: "background.paper"
      }}
    >
      <Stack direction="row" justifyContent="space-between" spacing={1.25} alignItems="flex-start">
        <Stack spacing={0.4}>
          <Typography variant="caption" sx={{ textTransform: "uppercase", letterSpacing: "0.08em" }}>
            {label}
          </Typography>
          <Typography variant="h2">{value}</Typography>
          {helper ? <Typography variant="caption">{helper}</Typography> : null}
        </Stack>
        <Box
          sx={{
            width: 38,
            height: 38,
            borderRadius: 3,
            display: "grid",
            placeItems: "center",
            bgcolor: alpha(chartColors.primary, 0.08),
            color: "primary.main"
          }}
        >
          {icon}
        </Box>
      </Stack>
    </Paper>
  );
}

function MetricPill({
  label,
  value,
  inverse
}: {
  label: string;
  value: number | null;
  inverse?: boolean;
}) {
  const tone = inverse ? passTone(value) : positiveTone(value);

  return (
    <Box
      sx={{
        minWidth: 82,
        px: 1.15,
        py: 0.8,
        borderRadius: 2.5,
        border: "1px solid",
        borderColor: tone.border,
        bgcolor: tone.bg
      }}
    >
      <Typography variant="caption" sx={{ display: "block", mb: 0.2 }}>
        {label}
      </Typography>
      <Typography variant="body2" sx={{ color: tone.fg, fontWeight: 700 }}>
        {formatPercent(value)}
      </Typography>
    </Box>
  );
}

function TypeOverviewPanel({ data }: { data: MetricsDashboardData["typeOverview"] }) {
  const maxItems = Math.max(...data.map((row) => row.totalItems), 1);

  return (
    <SectionFrame eyebrow="Production" title="Item type mix">
      <Stack spacing={1.4}>
        {data.map((row) => {
          const evaluatedShare = row.totalItems > 0 ? (row.evaluatedItems / row.totalItems) * 100 : 0;
          const lowAiShare = row.evaluatedItems > 0 ? (row.lowAiItems / row.evaluatedItems) * 100 : 0;

          return (
            <Box
              key={row.itemType}
              sx={{
                display: "grid",
                gridTemplateColumns: { xs: "1fr", lg: "220px 1fr auto" },
                gap: 1.5,
                alignItems: "center",
                border: "1px solid",
                borderColor: "divider",
                borderRadius: 3,
                px: 1.6,
                py: 1.4
              }}
            >
              <Stack spacing={0.2}>
                <Typography variant="body2" sx={{ color: "text.primary", fontWeight: 700 }}>
                  {itemTypeLabel(row.itemType)}
                </Typography>
                <Typography variant="caption">{row.totalItems} items</Typography>
              </Stack>

              <Stack spacing={1}>
                <Box sx={{ display: "flex", alignItems: "center", gap: 1 }}>
                  <Typography variant="caption" sx={{ minWidth: 38 }}>
                    Load
                  </Typography>
                  <Box sx={{ flex: 1, height: 10, borderRadius: 999, bgcolor: alpha(chartColors.primary, 0.08), overflow: "hidden" }}>
                    <Box
                      sx={{
                        width: `${countBarWidth(row.totalItems, maxItems)}%`,
                        height: "100%",
                        borderRadius: 999,
                        bgcolor: chartColors.primary
                      }}
                    />
                  </Box>
                </Box>
                <Box sx={{ display: "flex", alignItems: "center", gap: 1 }}>
                  <Typography variant="caption" sx={{ minWidth: 38 }}>
                    Eval
                  </Typography>
                  <Box sx={{ flex: 1, height: 10, borderRadius: 999, bgcolor: alpha(chartColors.parsons, 0.08), overflow: "hidden" }}>
                    <Box
                      sx={{
                        width: `${evaluatedShare}%`,
                        height: "100%",
                        borderRadius: 999,
                        bgcolor: chartColors.parsons
                      }}
                    />
                  </Box>
                </Box>
                <Box sx={{ display: "flex", alignItems: "center", gap: 1 }}>
                  <Typography variant="caption" sx={{ minWidth: 38 }}>
                    Low AI
                  </Typography>
                  <Box sx={{ flex: 1, height: 10, borderRadius: 999, bgcolor: alpha(chartColors.execution, 0.08), overflow: "hidden" }}>
                    <Box
                      sx={{
                        width: `${lowAiShare}%`,
                        height: "100%",
                        borderRadius: 999,
                        bgcolor: chartColors.execution
                      }}
                    />
                  </Box>
                </Box>
              </Stack>

              <Stack direction="row" spacing={0.8} flexWrap="wrap" useFlexGap>
                <MetricPill inverse label="AI" value={row.avgAiPassRate} />
                <MetricPill label="Student" value={row.avgStudentPassRate} />
              </Stack>
            </Box>
          );
        })}
      </Stack>
    </SectionFrame>
  );
}

function PipelinePanel({ data }: { data: MetricsDashboardData["pipeline"] }) {
  const rows = [
    { label: "GenConsistency", value: data.avgGenConsistencyRate },
    { label: "Q-Testsuite", value: data.avgQTestsuiteRate },
    { label: "Q-Context", value: data.avgQContextRate },
    { label: "PyTaskSyn-50", value: data.pyTaskSyn50Coverage }
  ];

  return (
    <SectionFrame eyebrow="Quality" title="Pipeline gates">
      <Stack spacing={1.2}>
        {rows.map((row) => (
          <Box key={row.label} sx={{ display: "grid", gridTemplateColumns: "124px 1fr 70px", gap: 1.1, alignItems: "center" }}>
            <Typography variant="body2" sx={{ color: "text.primary", fontWeight: 600 }}>
              {row.label}
            </Typography>
            <Box sx={{ height: 12, borderRadius: 999, bgcolor: alpha(chartColors.primary, 0.08), overflow: "hidden" }}>
              <Box
                sx={{
                  width: `${row.value ?? 0}%`,
                  height: "100%",
                  borderRadius: 999,
                  bgcolor: chartColors.primary
                }}
              />
            </Box>
            <Typography variant="body2" sx={{ textAlign: "right" }}>
              {formatPercent(row.value)}
            </Typography>
          </Box>
        ))}
      </Stack>
    </SectionFrame>
  );
}

function DistributionPanel({ data }: { data: MetricsDashboardData["aiPassDistribution"] }) {
  const maxTotal = Math.max(...data.map((bucket) => bucket.parsons + bucket.dropdown + bucket.executionTrace), 1);

  return (
    <SectionFrame
      eyebrow="Difficulty"
      title="AI pass buckets"
      action={
        <Stack direction="row" spacing={1} flexWrap="wrap" useFlexGap>
          <Chip label="Parsons" size="small" sx={{ bgcolor: alpha(chartColors.parsons, 0.12), color: chartColors.parsons, borderColor: alpha(chartColors.parsons, 0.16) }} />
          <Chip label="Dropdown" size="small" sx={{ bgcolor: alpha(chartColors.dropdown, 0.12), color: chartColors.dropdown, borderColor: alpha(chartColors.dropdown, 0.16) }} />
          <Chip label="Trace" size="small" sx={{ bgcolor: alpha(chartColors.execution, 0.12), color: chartColors.execution, borderColor: alpha(chartColors.execution, 0.16) }} />
        </Stack>
      }
    >
      <Stack spacing={1.2}>
        {data.map((bucket) => {
          const total = bucket.parsons + bucket.dropdown + bucket.executionTrace;
          return (
            <Box key={bucket.bucket} sx={{ display: "grid", gridTemplateColumns: "70px 1fr 42px", gap: 1, alignItems: "center" }}>
              <Typography variant="body2" sx={{ color: "text.primary", fontWeight: 700 }}>
                {bucket.bucket}
              </Typography>
              <Box sx={{ display: "flex", gap: 0.5, height: 16 }}>
                <Box
                  sx={{
                    width: `${countBarWidth(bucket.parsons, maxTotal)}%`,
                    minWidth: bucket.parsons ? 8 : 0,
                    bgcolor: chartColors.parsons,
                    borderRadius: 999
                  }}
                />
                <Box
                  sx={{
                    width: `${countBarWidth(bucket.dropdown, maxTotal)}%`,
                    minWidth: bucket.dropdown ? 8 : 0,
                    bgcolor: chartColors.dropdown,
                    borderRadius: 999
                  }}
                />
                <Box
                  sx={{
                    width: `${countBarWidth(bucket.executionTrace, maxTotal)}%`,
                    minWidth: bucket.executionTrace ? 8 : 0,
                    bgcolor: chartColors.execution,
                    borderRadius: 999
                  }}
                />
              </Box>
              <Typography variant="caption" sx={{ textAlign: "right" }}>
                {total}
              </Typography>
            </Box>
          );
        })}
      </Stack>
    </SectionFrame>
  );
}

function QueryHeatmapPanel({ data }: { data: MetricsDashboardData["queryOverview"] }) {
  const maxSourceTasks = Math.max(...data.map((row) => row.sourceTaskCount), 1);
  const maxTypedItems = Math.max(...data.map((row) => row.typedItemCount), 1);
  const maxPyTaskSyn = Math.max(...data.map((row) => row.pyTaskSyn50Count), 1);

  const CountCell = ({
    value,
    maxValue,
    tone
  }: {
    value: number;
    maxValue: number;
    tone: string;
  }) => (
    <Box
      sx={{
        borderRadius: 2.2,
        px: 0.8,
        py: 0.75,
        textAlign: "center",
        bgcolor: alpha(tone, 0.08 + (value / maxValue) * 0.22),
        color: tone,
        fontSize: "0.82rem",
        fontWeight: 700
      }}
    >
      {value}
    </Box>
  );

  const PercentCell = ({
    value,
    inverse
  }: {
    value: number | null;
    inverse?: boolean;
  }) => {
    const tone = inverse ? passTone(value) : positiveTone(value);
    return (
      <Box
        sx={{
          borderRadius: 2.2,
          px: 0.8,
          py: 0.75,
          textAlign: "center",
          bgcolor: tone.bg,
          border: "1px solid",
          borderColor: tone.border,
          color: tone.fg,
          fontSize: "0.82rem",
          fontWeight: 700
        }}
      >
        {formatPercent(value)}
      </Box>
    );
  };

  return (
    <SectionFrame eyebrow="Coverage by query" title="Query heatmap">
      <Box sx={{ overflowX: "auto" }}>
        <Box sx={{ minWidth: 760, display: "grid", gap: 0.8 }}>
          <Box
            sx={{
              display: "grid",
              gridTemplateColumns: "104px repeat(7, minmax(76px, 1fr))",
              gap: 0.7
            }}
          >
            {["Query", "Source", "Typed", "Low AI", "Avg AI", "Student", "Q-Test", "Py50"].map((label) => (
              <Typography key={label} variant="caption" sx={{ px: 0.25 }}>
                {label}
              </Typography>
            ))}
          </Box>

          {data.map((row) => (
            <Box
              key={row.queryId}
              sx={{
                display: "grid",
                gridTemplateColumns: "104px repeat(7, minmax(76px, 1fr))",
                gap: 0.7,
                alignItems: "center"
              }}
            >
              <Typography variant="body2" sx={{ color: "text.primary", fontWeight: 700, px: 0.25 }}>
                {row.queryId}
              </Typography>
              <CountCell maxValue={maxSourceTasks} tone={chartColors.primary} value={row.sourceTaskCount} />
              <CountCell maxValue={maxTypedItems} tone={chartColors.parsons} value={row.typedItemCount} />
              <CountCell maxValue={maxTypedItems} tone={chartColors.execution} value={row.lowAiItemCount} />
              <PercentCell inverse value={row.avgAiPassRate} />
              <PercentCell value={row.avgStudentPassRate} />
              <PercentCell value={row.qTestsuiteRate} />
              <CountCell maxValue={maxPyTaskSyn} tone={chartColors.dropdown} value={row.pyTaskSyn50Count} />
            </Box>
          ))}
        </Box>
      </Box>
    </SectionFrame>
  );
}

function ThemeBarsPanel({ data }: { data: MetricsDashboardData["themeOverview"] }) {
  const maxItems = Math.max(...data.map((row) => row.totalItems), 1);
  const topThemes = data.slice(0, 8);

  return (
    <SectionFrame eyebrow="Themes" title="Theme spread">
      <Stack spacing={1.15}>
        {topThemes.map((row) => (
          <Box key={row.theme} sx={{ display: "grid", gridTemplateColumns: "120px 1fr auto", gap: 1, alignItems: "center" }}>
            <Typography noWrap variant="body2" sx={{ color: "text.primary", fontWeight: 600 }}>
              {row.theme}
            </Typography>
            <Box sx={{ display: "flex", gap: 0.5, height: 14 }}>
              <Box
                sx={{
                  width: `${countBarWidth(row.totalItems, maxItems)}%`,
                  bgcolor: chartColors.primary,
                  borderRadius: 999
                }}
              />
              <Box
                sx={{
                  width: `${countBarWidth(row.lowAiItems, maxItems)}%`,
                  bgcolor: chartColors.execution,
                  borderRadius: 999
                }}
              />
            </Box>
            <Chip label={formatPercent(row.avgAiPassRate)} size="small" />
          </Box>
        ))}
        <Stack direction="row" spacing={1} flexWrap="wrap" useFlexGap sx={{ pt: 0.4 }}>
          <Chip label="Total items" size="small" sx={{ bgcolor: alpha(chartColors.primary, 0.12), color: chartColors.primary, borderColor: alpha(chartColors.primary, 0.16) }} />
          <Chip label="Low-AI items" size="small" sx={{ bgcolor: alpha(chartColors.execution, 0.12), color: chartColors.execution, borderColor: alpha(chartColors.execution, 0.16) }} />
        </Stack>
      </Stack>
    </SectionFrame>
  );
}

function TelemetryPanel({ data }: { data: MetricsDashboardData["telemetry"] }) {
  if (!data.available) {
    return (
      <SectionFrame
        eyebrow="Telemetry"
        title="No student interaction data"
        action={
          <Button component={Link} endIcon={<ArrowForwardRounded fontSize="small" />} href="/" variant="outlined">
            Open student mode
          </Button>
        }
      >
        <Box
          sx={{
            borderRadius: 3,
            border: "1px dashed",
            borderColor: "divider",
            px: 2,
            py: 3.5,
            textAlign: "center"
          }}
        >
          <Typography variant="body2">
            Complete a few student-mode attempts first. This panel will then fill with attempt counts, event volumes, focus exits, and score patterns.
          </Typography>
        </Box>
      </SectionFrame>
    );
  }

  const maxEventCount = Math.max(...data.eventBreakdown.map((row) => row.count), 1);

  return (
    <SectionFrame eyebrow="Student telemetry" title="Interaction signals">
      <Box sx={{ display: "grid", gridTemplateColumns: { xs: "1fr", xl: "0.88fr 1.12fr" }, gap: 1.5 }}>
        <Box sx={{ display: "grid", gap: 1.2 }}>
          <Box sx={{ display: "grid", gridTemplateColumns: { xs: "repeat(2, minmax(0, 1fr))", md: "repeat(4, minmax(0, 1fr))" }, gap: 1.2 }}>
            <StatCard helper="formal submissions" icon={<AssessmentRounded fontSize="small" />} label="Attempts" value={formatCompactNumber(data.totalAttempts)} />
            <StatCard helper="captured interactions" icon={<InsightsRounded fontSize="small" />} label="Events" value={formatCompactNumber(data.totalEvents)} />
            <StatCard helper="mean active attempt" icon={<AutoGraphRounded fontSize="small" />} label="Avg time" value={formatDuration(data.avgAttemptDurationMs)} />
            <StatCard helper="submission quality" icon={<ShieldRounded fontSize="small" />} label="Avg score" value={formatPercent(data.avgAttemptScore)} />
          </Box>

          <Paper sx={{ p: 2, borderRadius: 3 }}>
            <Stack spacing={1.15}>
              <Stack direction="row" justifyContent="space-between">
                <Typography variant="h3">Integrity signals</Typography>
                <Stack direction="row" spacing={1}>
                  <Chip label={`${data.focusLossCount} exits`} size="small" />
                  <Chip label={`${data.resumeCount} resumes`} size="small" />
                </Stack>
              </Stack>
              <Box sx={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 1 }}>
                <Box sx={{ border: "1px solid", borderColor: "divider", borderRadius: 3, p: 1.4 }}>
                  <Typography variant="caption">Recent focus exits</Typography>
                  <Typography sx={{ color: chartColors.warning, fontSize: "1.5rem", fontWeight: 700, lineHeight: 1.1 }}>
                    {data.focusLossCount}
                  </Typography>
                </Box>
                <Box sx={{ border: "1px solid", borderColor: "divider", borderRadius: 3, p: 1.4 }}>
                  <Typography variant="caption">Latest activity</Typography>
                  <Typography sx={{ color: chartColors.primary, fontSize: "0.98rem", fontWeight: 700, lineHeight: 1.3 }}>
                    {data.recentFocusEvents[0] ? formatDateTime(data.recentFocusEvents[0].eventTime) : "No exits yet"}
                  </Typography>
                </Box>
              </Box>
            </Stack>
          </Paper>
        </Box>

        <Paper sx={{ p: 2, borderRadius: 3 }}>
          <Stack spacing={1.15}>
            <Stack direction="row" justifyContent="space-between">
              <Typography variant="h3">Event volume</Typography>
              <Chip icon={<BoltRounded fontSize="small" />} label={`${data.eventBreakdown.length} tracked events`} size="small" />
            </Stack>
            {data.eventBreakdown.slice(0, 8).map((event) => (
              <Box key={event.eventType} sx={{ display: "grid", gridTemplateColumns: "140px 1fr 42px", gap: 1, alignItems: "center" }}>
                <Typography noWrap variant="caption">
                  {event.eventType}
                </Typography>
                <Box sx={{ height: 12, borderRadius: 999, bgcolor: alpha(chartColors.primary, 0.08), overflow: "hidden" }}>
                  <Box
                    sx={{
                      width: `${countBarWidth(event.count, maxEventCount)}%`,
                      height: "100%",
                      borderRadius: 999,
                      bgcolor: chartColors.primary
                    }}
                  />
                </Box>
                <Typography variant="caption" sx={{ textAlign: "right" }}>
                  {event.count}
                </Typography>
              </Box>
            ))}
          </Stack>
        </Paper>
      </Box>
    </SectionFrame>
  );
}

export default async function MetricsPage() {
  const data = await getMetricsDashboardData();

  return (
    <Box
      sx={{
        minHeight: "100vh",
        bgcolor: "background.default",
        color: "text.primary"
      }}
    >
      <Box
        sx={{
          position: "sticky",
          top: 0,
          zIndex: 20,
          backdropFilter: "blur(18px)",
          bgcolor: alpha("#F6F8FB", 0.86),
          borderBottom: "1px solid",
          borderColor: "divider"
        }}
      >
        <Box
          sx={{
            maxWidth: 1800,
            mx: "auto",
            px: { xs: 2, md: 4 },
            py: 1.35,
            display: "flex",
            alignItems: "center",
            justifyContent: "space-between",
            gap: 2
          }}
        >
          <Stack spacing={0.25}>
            <Typography variant="body2" sx={{ color: "primary.main", fontWeight: 700 }}>
              Learning Analytics
            </Typography>
            <Typography variant="caption">Updated {formatDateTime(data.generatedAt)}</Typography>
          </Stack>
          <Button component={Link} href="/" variant="outlined" endIcon={<NorthEastRounded fontSize="small" />}>
            Student mode
          </Button>
        </Box>
      </Box>

      <Box sx={{ maxWidth: 1800, mx: "auto", px: { xs: 2, md: 4 }, py: { xs: 2.5, md: 3.25 } }}>
        <Stack spacing={2}>
          <Stack
            direction={{ xs: "column", lg: "row" }}
            justifyContent="space-between"
            alignItems={{ xs: "flex-start", lg: "center" }}
            spacing={1.5}
          >
            <Stack spacing={0.3}>
              <Typography variant="h1">Learning analytics dashboard</Typography>
              <Typography variant="body2">A compact board for typed-item quality, assistant difficulty, and student activity.</Typography>
            </Stack>
            <Stack direction="row" spacing={1} flexWrap="wrap" useFlexGap>
              <Chip color="primary" label={`${data.totals.queries} queries`} />
              <Chip label={`${data.totals.evaluatedItems} evaluated`} />
              <Chip label={`${data.totals.telemetryAttempts} attempts`} />
            </Stack>
          </Stack>

          <Box sx={{ display: "grid", gridTemplateColumns: { xs: "repeat(2, minmax(0, 1fr))", xl: "repeat(4, minmax(0, 1fr))" }, gap: 1.25 }}>
            <StatCard
              helper={`${formatCompactNumber(data.totals.sourceTasks)} source tasks`}
              icon={<QueryStatsRounded fontSize="small" />}
              label="Inventory"
              value={formatCompactNumber(data.totals.typedItems)}
            />
            <StatCard
              helper={`${formatCompactNumber(data.totals.lowAiItems)} low-AI items`}
              icon={<AutoGraphRounded fontSize="small" />}
              label="Evaluated"
              value={`${data.totals.evaluatedItems}/${data.totals.typedItems}`}
            />
            <StatCard
              helper={`student ${formatPercent(data.totals.avgStudentPassRate)}`}
              icon={<InsightsRounded fontSize="small" />}
              label="AI pass"
              value={formatPercent(data.totals.avgAiPassRate)}
            />
            <StatCard
              helper={`${data.totals.telemetryEvents} events · ${data.telemetry.focusLossCount} exits`}
              icon={<ShieldRounded fontSize="small" />}
              label="Telemetry"
              value={formatCompactNumber(data.totals.telemetryAttempts)}
            />
          </Box>

          <Box sx={{ display: "grid", gridTemplateColumns: { xs: "1fr", xl: "1.05fr 0.95fr" }, gap: 1.5 }}>
            <TypeOverviewPanel data={data.typeOverview} />
            <DistributionPanel data={data.aiPassDistribution} />
          </Box>

          <Box sx={{ display: "grid", gridTemplateColumns: { xs: "1fr", xl: "1.24fr 0.76fr" }, gap: 1.5 }}>
            <QueryHeatmapPanel data={data.queryOverview} />
            <PipelinePanel data={data.pipeline} />
          </Box>

          <Box sx={{ display: "grid", gridTemplateColumns: { xs: "1fr", xl: "1fr" }, gap: 1.5 }}>
            <ThemeBarsPanel data={data.themeOverview} />
          </Box>

          <TelemetryPanel data={data.telemetry} />
        </Stack>
      </Box>
    </Box>
  );
}
