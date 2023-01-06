function linkFormatter(value, row) {
    return `<a href='/-/kb/vmdr/view?qid=${row.qid}'>` + value + "</a>";
}

searchText = "";

$(function(){
    $("#searchForm").submit(function(e){
        e.preventDefault();
        searchText = $("#searchField").val()
        $("#kbVmdrTable").bootstrapTable('refresh')
    })
})

function ajaxRequest(params) {
    if (searchText){
        params.data['search'] = searchText;
    }
    $.get(vmdrUrl + '?' + $.param(params.data)).then(function (res) {
        params.success(res)
    })
}