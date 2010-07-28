fun_get_old_hosts = \
"""
function(doc) {
    if(!doc.age) {
        emit(doc._id);
    } else if(doc.age < "%s") {
        emit(doc._id);
    }
}
"""

fun_gen_doc_index = \
"""
function(doc) {
    doc.files.map(
        function(file) {
            var lower = file.toLowerCase();
            var tokens = lower.split(/[^-A-Za-z0-9_]+/);
            tokens.map(
                function(token) {
                    emit(token, doc._id);
                }
            )
        }
    )
}
"""
