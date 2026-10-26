import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', name: 'home', component: () => import('@/views/HomeView.vue'), meta: { title: '模拟面试' } },
    { path: '/interview/:jobId?', name: 'interview', component: () => import('@/views/InterviewView.vue'), meta: { title: '面试进行中' } },
    { path: '/report/:id?', name: 'report', component: () => import('@/views/ReportView.vue'), meta: { title: '面试报告' } },
    { path: '/dashboard', name: 'dashboard', component: () => import('@/views/DashboardView.vue'), meta: { title: '能力看板' } },
    { path: '/settings', name: 'settings', component: () => import('@/views/SettingsView.vue'), meta: { title: '模型设置' } },
    { path: '/help', name: 'help', component: () => import('@/views/HelpView.vue'), meta: { title: '帮助中心' } }
  ]
})

export default router
