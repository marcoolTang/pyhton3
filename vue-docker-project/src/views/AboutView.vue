<template>
  <div class="about">
    <h1>This is an about page</h1>
    <form @submit.prevent="submitForm">
      <label for="name">Name:</label>
      <input type="text" id="name" v-model="name" required>
      <label for="age">Age:</label>
      <input type="number" id="age" v-model="age" required>
      <button type="submit">Submit</button>
    </form>
    <table v-if="submittedData.length > 0">
      <thead>
        <tr>
          <th>Name</th>
          <th>Age</th>
          <th>Action</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(data, index) in submittedData" :key="index">
          <td>{{ data.name }}</td>
          <td>{{ data.age }}</td>
          <td>
            <button @click="deleteItem(data.id)">Delete</button>
            <button @click="updateItem(data)">Update</button>
          </td>
        </tr>
      </tbody>
    </table>
    <div v-show="isShowUpdateModal">
      <form @submit.prevent="updateData">
        <label for="name">Name:</label>
        <input type="text" id="name" v-model="updateName" required>
        <label for="age">Age:</label>
        <input type="number" id="age" v-model="updateAge" required>
        <button type="submit">Submit</button>
    </form>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

let host = import.meta.env.VITE_API_URL;
console.log( import.meta.env)

export default {
  data() {
    return {
      name: '',
      age: '',
      updateName:'',
      updateAge:'',
      submittedData: [],
      isShowUpdateModal:false,
      currentItemId:null,
    };
  },
  created() {
    // 页面创建时请求数据
    this.getData();
  },
  methods: {
    async getData() {
      try {
        const response = await axios.get(host + '/api/getData');
        // 假设后台返回的数据结构为 { success: true, data: [{ id: ..., name: '...', age: '...' }, ...] }
        if (response.data.success) {
          this.submittedData = response.data.data;
        } else {
          console.error('Get data failed:', response.data.error);
        }
      } catch (error) {
        console.error('Get data error:', error);
      }
    },
    async submitForm() {
      try {
        const response = await axios.post(host + '/api/addData', { name: this.name, age: this.age });
        // 假设后台返回的数据结构为 { success: true, data: { id: ..., name: '...', age: '...' } }
        if (response.data.success) {
          this.submittedData = response.data.data
          // 清空输入框
          this.name = '';
          this.age = '';
        } else {
          console.error('Add name failed:', response.data.error);
        }
      } catch (error) {
        console.error('Add name error:', error);
      }
    },
    async deleteItem(id) {
      try {
        const response = await axios.get(host + `/api/deleteData?id=${id}`);
        if (response.data.success) {
          // 从 submittedData 中移除被删除的项
          this.submittedData = this.submittedData.filter(item => item.id !== id);
        } else {
          console.error('Delete item failed:', response.data.error);
        }
      } catch (error) {
        console.error('Delete item error:', error);
      }
    },
    updateItem(data) {
      // 在这里处理更新数据的逻辑，例如弹出一个模态框进行编辑
      if(data.id  != this.currentItemId && this.isShowUpdateModal){
      }else{
        this.isShowUpdateModal = !this.isShowUpdateModal
      }
      this.currentItemId = data.id;
      this.updateName = data.name;
      this.updateAge = data.age;
      
      
    },
    async updateData(data) {
        
      // 在这里处理更新数据的逻辑，例如弹出一个模态框进行编辑
      try {
        const response = await axios.post(host + `/api/updateData`, {id:this.currentItemId, name: this.updateName, age: this.updateAge });
        if (response.data.success) {
          // 更新成功后更新前端展示的数据
      
            this.submittedData = response.data.data;
          
        } else {
          console.error('Update item failed:', response.data.error);
        }
      } catch (error) {
        console.error('Update item error:', error);
      }
      
      
    }
  }
};
</script>

<style>
@media (min-width: 1024px) {
  .about {
    min-height: 100vh;
    display: flex;
    align-items: center;
    flex-direction: column;
  }
  table {
    margin-top: 20px;
    border-collapse: collapse;
    width: 50%;
  }
  th, td {
    border: 1px solid #ddd;
    padding: 8px;
    text-align: left;
  }
  th {
    background-color: #f2f2f2;
  }
}
</style>
