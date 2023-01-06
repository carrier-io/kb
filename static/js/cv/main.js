function linkFormatter(value, row) {
    return `<a href='/-/kb/cv/view?cid=${row.cid}'>` + value + "</a>";
}

searchText = "";

$(function(){
    $("#searchForm").submit(function(e){
        e.preventDefault();
        searchText = $("#searchField").val()
        $("#kbCVTable").bootstrapTable('refresh')
    })
})

function ajaxRequest(params) {
    if (searchText){
        params.data['search'] = searchText;
    }
    $.get(cvUrl + '?' + $.param(params.data)).then(function (res) {
        params.success(res)
    })
}