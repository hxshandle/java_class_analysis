;(function () {
  const BASE_URL = 'http://hh.test'
  const loading = $('#loading')
  const tabNav = $('#pills-tab')
  const tabs = ['mindmap', 'sequence', 'repo']
  var diagrams = {
    mindmap: null,
    sequence: null,
    repo: null
  }
  var data = null
  var isProcessing = false

  function toggleLoading() {
    loading.toggleClass('d-none')
  }

  function resetDiagram(){
    diagrams = {
      mindmap: null,
      sequence: null,
      repo: null
    }
  }

  function do_query() {
    if (isProcessing) {
      return
    }
    resetDiagram()
    className = $('#class-name').val()
    isProcessing = true
    console.log('do query ' + className)
    toggleLoading()
    $.ajax({
      url: `${BASE_URL}/code_analysis/query`,
      type: 'post',
      dataType: 'json',
      data: JSON.stringify({
        name: className,
        method: null,
      }),
      headers: {
        'content-type': 'application/json;charset=UTF-8',
      },
      error: function () {
        console.log('Error')
        toggleLoading()
      },
      success: function (response) {
        data = response
        toggleLoading()
        renderTab(0)
      },
    })
    isProcessing = false
  }

  function renderTab(index) {
    targetTab = tabs[index]
    var settings = {
      url: `${BASE_URL}/uml/`,
      type: 'post',
      headers: {
        'Content-Type': 'text/plain;charset=UTF-8',
      },
      data: data[targetTab],
      success: function (response) {
        $(`#${targetTab}-svg-wrapper`).get(0).innerHTML = response
        diagrams[tabs[index]] = response
      },
      error: function () {},
    }
    $.ajax(settings)
  }

  function on_enter_key_in_class_name(event) {
    if (event.keyCode == 13) {
      do_query()
    }
  }

  $('a[data-bs-toggle="pill"]').forEach((element) => {
    element.addEventListener('shown.bs.tab', function (event) {
      target = event.target.id.split('-')[1]
      if (diagrams[target] == null) {
        renderTab(tabs.indexOf(target))
      }
    })
  })

  $('#button-go').on('click', do_query)
  $('#class-name').on('keypress', on_enter_key_in_class_name)
})()
