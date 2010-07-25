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
