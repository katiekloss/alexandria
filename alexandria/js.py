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
    for(var i in doc.files) {
        var file = doc.files[i].toLowerCase();
        var tokens = file.split(/[^-A-Za-z0-9_]+/);
        tokens.map(
            function(token) {
                emit(token, i);
            }
        )
    }
}
"""
