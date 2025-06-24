var dmcfuncs = window.dashMantineFunctions = window.dashMantineFunctions || {};

dmcfuncs.formatNumberIntl = (value) => {
  const absValue = Math.abs(value);
  let formatted;

  if (absValue >= 1_000_000_000) {
    formatted = (value / 1_000_000_000).toPrecision(3) + "B";
  } else if (absValue >= 1_000_000) {
    formatted = (value / 1_000_000).toPrecision(3) + "M";
  } else if (absValue >= 1_000) {
    formatted = (value / 1_000).toPrecision(3) + "K";
  } else {
    formatted = value.toString();
  }

  return "$" + formatted;
};
