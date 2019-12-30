$(function () {
    $('#dataTable').DataTable({
        fnDrawCallback: function(oSettings) {
            let totalPages = this.api().page.info().pages;
            if(!totalPages | totalPages == 1){
                $('.dataTables_paginate').hide(); 
            }
            else { 
                $('.dataTables_paginate').show(); 
            }
        },
        "language": {
            "url": "../../../static/js/datatable_i18n.json"
        },
    });
  
  $('[data-toggle="tooltip"]').tooltip()
})