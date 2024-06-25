$(document).ready(function(){
    $(document).on('click', '.pagination a', function(e){
        e.preventDefault();

        var page = $(this).attr('href').split('page=')[1];
        $.ajax({
            url: '?page=' + page,
            success: function(data) {
                var tableBody = $(data.pagination_table);
                $('#table-body').html(tableBody);

                var paginationBar = $(data.pagination_bar);
                $('#pagination-container').html(paginationBar);
            }
        });
    });
});