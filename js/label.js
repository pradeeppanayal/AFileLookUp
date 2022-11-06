export default {
    props:['label','allowdelete'],
    template:`<li class="list-group-item d-flex justify-content-between align-items-center">
                    {{label.text}}
                    <i v-if="allowdelete" style="cursor:pointer;" @click="deleteLabel" title="Delete" class="material-icons">delete</i>
            </li>`,
    methods:{
        deleteLabel:function(){
            this.$emit('delete',this.label)
        }
    }
}