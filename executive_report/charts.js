const { totals, municipalities, regions, route58, hours, lighting, types } = reportData;
const count = d3.format(",");
const percent = d3.format(".2%");
const css = getComputedStyle(document.documentElement);

function color(name) {
  return css.getPropertyValue(name).trim();
}

function setText(id, value) {
  document.getElementById(id).textContent = value;
}

// Fill the figures used in the report copy.
d3.selectAll("[data-metric]").text(function () {
  return count(totals[this.dataset.metric]);
});

const regionalCrashes = d3.sum(
  regions.filter(row => ["South", "Central"].includes(row.label)),
  row => row.crashes
);
const fullNight = lighting.find(row => row.code === 22);
const fullDaylight = lighting.find(row => row.code === 12);
const pedestrian = types.find(row => row.label === "Pedestrian–vehicle");
const vehicles = types.find(row => row.label === "Vehicle–vehicle");
const weekdayHours = hours.filter(row => row.day >= 2 && row.day <= 6);
const weekdayCrashesByHour = d3.rollups(weekdayHours, rows => d3.sum(rows, row => row.crashes), row => row.hour);
const morningPeak = d3.greatest(weekdayCrashesByHour.filter(([hour]) => hour < 12), ([, crashes]) => crashes);
const afternoonPeak = d3.greatest(weekdayCrashesByHour.filter(([hour]) => hour >= 12), ([, crashes]) => crashes);
const time = hour => `${hour % 12 || 12} ${hour < 12 ? "a.m." : "p.m."}`;
const peakLabel = ([hour, crashes]) => `${count(crashes)} crashes during the ${time(hour)} hour`;

setText("regional-count", count(regionalCrashes));
setText("route-count", count(route58.crashes));
setText("night-deaths", `${count(fullNight.deaths)} of ${count(totals.deaths)}`);
setText("night-crashes", count(fullNight.crashes));
setText("morning-peak", peakLabel(morningPeak));
setText("afternoon-peak", peakLabel(afternoonPeak));
setText("pedestrian-fatal", count(pedestrian.fatal_crashes));
setText("vehicle-share", d3.format(".1%")(vehicles.crashes / totals.crashes));

// Horizontal bars have visible labels and a shared zero baseline within each chart.
function drawBars(target, rows, format) {
  const width = d3.scaleLinear()
    .domain([0, d3.max(rows, row => row.value)])
    .range([0, 100]);

  const bars = d3.select(target).selectAll(".bar-row").data(rows).join("div")
    .attr("class", "bar-row");

  const labels = bars.append("div").attr("class", "bar-label");
  labels.append("span").text(row => row.label);
  labels.append("span").attr("class", "bar-value").text(format);

  const tracks = bars.append("svg")
    .attr("class", "bar-track")
    .attr("aria-hidden", "true");

  tracks.append("rect")
    .attr("width", "100%")
    .attr("height", "100%")
    .attr("fill", color("--heat-low"));

  tracks.append("rect")
    .attr("width", row => `${width(row.value)}%`)
    .attr("height", "100%")
    .attr("rx", 3)
    .attr("fill", row => color(row.fill));
}

drawBars("#municipalities", municipalities.map((row, index) => ({
  label: row.label,
  value: row.crashes,
  fill: index === 0 ? "--blue" : "--blue-muted"
})), row => count(row.value));

drawBars("#lighting", [fullNight, fullDaylight].map(row => ({
  label: row.code === 22 ? "Full darkness" : "Full daylight",
  value: row.fatal_crashes / row.crashes,
  detail: `${count(row.fatal_crashes)} of ${count(row.crashes)}`,
  fill: row.code === 22 ? "--red" : "--red-muted"
})), row => `${percent(row.value)} · ${row.detail}`);

drawBars("#types", types.map((row, index) => ({
  label: row.label,
  value: row.fatal_crashes,
  fill: index === 0 ? "--red" : "--red-muted"
})), row => count(row.value));

// Day-by-hour heatmap. One tab stop enters the chart, and arrow keys move between cells.
const dayNames = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];
const heatWidth = 1040;
const heatHeight = 209;
const x = d3.scaleBand().domain(d3.range(24)).range([51, heatWidth - 4]).paddingInner(0.10);
const y = d3.scaleBand().domain(d3.range(1, 8)).range([24, heatHeight - 4]).paddingInner(0.13);
const maxCell = d3.max(hours, row => row.crashes);
const heatColor = d3.scaleSequential([0, maxCell], d3.interpolateRgb(color("--heat-low"), color("--heat-high")));

setText("heat-max", maxCell);
d3.select(".heat-gradient").style("background", `linear-gradient(90deg, ${heatColor(0)}, ${heatColor(maxCell)})`);

const heatmap = d3.select("#heatmap").append("svg")
  .attr("viewBox", `0 0 ${heatWidth} ${heatHeight}`)
  .attr("role", "group")
  .attr("aria-label", "Recorded crashes by day of week and hour, in local time");

const hourLabel = hour => `${String(hour).padStart(2, "0")}:00`;
const cellLabel = row => `${dayNames[row.day - 1]} · ${hourLabel(row.hour)} · ${row.crashes} recorded ${row.crashes === 1 ? "crash" : "crashes"}`;
const detail = document.getElementById("heat-detail");
const defaultDetail = detail.textContent;

heatmap.append("g").attr("aria-hidden", "true").selectAll("text")
  .data(d3.range(0, 24, 3)).join("text")
  .attr("class", "heat-label")
  .attr("text-anchor", "middle")
  .attr("x", hour => x(hour) + x.bandwidth() / 2)
  .attr("y", 15)
  .text(hourLabel);

heatmap.append("g").attr("aria-hidden", "true").selectAll("text")
  .data(y.domain()).join("text")
  .attr("class", "heat-label")
  .attr("x", 1)
  .attr("y", day => y(day) + y.bandwidth() / 2)
  .attr("dominant-baseline", "central")
  .text(day => dayNames[day - 1].slice(0, 3));

const steps = { ArrowLeft: [0, -1], ArrowRight: [0, 1], ArrowUp: [-1, 0], ArrowDown: [1, 0] };

const cells = heatmap.append("g").selectAll("rect").data(hours).join("rect")
  .attr("class", "heat-cell")
  .attr("role", "img")
  .attr("aria-label", cellLabel)
  .attr("tabindex", (_, index) => index === 0 ? 0 : -1)
  .attr("x", row => x(row.hour))
  .attr("y", row => y(row.day))
  .attr("width", x.bandwidth())
  .attr("height", y.bandwidth())
  .attr("rx", 3)
  .attr("fill", row => heatColor(row.crashes))
  .on("pointerenter focus", (_, row) => { detail.textContent = cellLabel(row); })
  .on("pointerleave blur", () => { detail.textContent = defaultDetail; })
  .on("click", function () { focusCell(this); })
  .on("keydown", (event, row) => {
    const step = steps[event.key];
    if (!step) return;
    event.preventDefault();
    const day = Math.max(1, Math.min(7, row.day + step[0]));
    const hour = Math.max(0, Math.min(23, row.hour + step[1]));
    focusCell(cells.nodes()[(day - 1) * 24 + hour]);
  });

function focusCell(cell) {
  cells.attr("tabindex", -1);
  cell.setAttribute("tabindex", "0");
  cell.focus();
}
