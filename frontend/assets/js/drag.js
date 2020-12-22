var isDrag = false
var startPos = null
var mouseStartPos = null
var svgEl = null

var viewDim = $('.tab-panel-content')
$('.mask').on('mousedown', function (event) {
  isDrag = true
  svgEl = event.target.nextElementSibling.children[0]
  viewEl = event.target.parentElement
  var xPos = svgEl.style.left == '' ? '0' : svgEl.style.left
  var yPos = svgEl.style.top == '' ? '0' : svgEl.style.top
  startPos = [
    parseInt(xPos),
    parseInt(yPos),
    parseInt(svgEl.getAttribute('width')), // svg width
    parseInt(svgEl.getAttribute('height')), // svg height
    viewEl.offsetWidth, // view port width
    viewEl.offsetHeight, // view port height
  ]
  mouseStartPos = [event.clientX, event.clientY]
  // console.log(`start POS ${startPos}`)
  // console.log(`start Mouse POS ${mouseStartPos}`)
})

$('.mask').on('mouseup', function (event) {
  document.body.style.cursor = 'default'
  isDrag = false
  startPos = null
  mouseStartPos = null
  svgEl = null
})

$('.mask').on('mousemove', function (event) {
  if (!isDrag) {
    return
  }
  var xOffset = event.clientX - mouseStartPos[0]
  var yOffset = event.clientY - mouseStartPos[1]
  var x = startPos[0] + xOffset
  var y = startPos[1] + yOffset
  x = Math.max(-( startPos[2] - startPos[4]), x)
  y = Math.max(-( startPos[3] - startPos[5]), y)
  x = Math.min(x, 0)
  y = Math.min(y, 0)
  svgEl.style.left = x
  svgEl.style.top = y
  // console.log(event)
})
