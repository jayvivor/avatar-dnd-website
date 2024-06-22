$(document).ready(function(){
    $(document).on('click', '.pagination a', function(e){
        e.preventDefault();
        var page = $(this).attr('href').split('page=')[1];
        $.ajax({
            url: '?page=' + page,
            success: function(data) {
                var items = data.items;
                var tableBody = '';
                for (var i = 0; i < items.length; i++) {
                    tableBody += '<tr><td>' + items[i].field1 + '</td><td>' + items[i].field2 + '</td></tr>';
                }
                $('#table-body').html(tableBody);

                var paginationHtml = $(data.pagination_html);
                $('#pagination-container').html(paginationHtml);
            }
        });
    });
});