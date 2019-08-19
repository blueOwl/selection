draw_a_line_init = function (y, color, ylim) {
  if (missing(ylim)) {
    ylim = c(min(y) - 10, max(y) + 10)
  }
  if (missing(color)) {
    color = 'red'
  }
  plot(seq(length(y)), y, col=color, ylim=ylim)
}
draw_a_line_add = function (y, color = 'red') {
  points(seq(length(y)), y, col=color)
}

#y_sim = ceiling(runif(400) * 5000)
y_sim = rep(10,5000)
draw_a_line_init(y_sim)
y_sim = rep(11,5000)
draw_a_line_add(y_sim, color='blue')