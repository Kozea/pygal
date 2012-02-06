from pygal.style import Style


def test_colors():
    style = Style(colors=['red', '#231A3b', '#ff0', 'rgb(12, 231, 3)'])
    assert style.colors == '''\
.color-0 {
  stroke: red;
  fill: red;
}

.color-1 {
  stroke: #231A3b;
  fill: #231A3b;
}

.color-2 {
  stroke: #ff0;
  fill: #ff0;
}

.color-3 {
  stroke: rgb(12, 231, 3);
  fill: rgb(12, 231, 3);
}
'''
