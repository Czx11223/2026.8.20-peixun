/** @type {import('tailwindcss').Config} */
// 面知 Design System — 极简蓝调 (Apple 变体)
// 设计约束：无阴影、主色 #007AFF、双字重(400/600)、四级圆角、8px 栅格
export default {
  content: ['./index.html', './src/**/*.{vue,ts}'],
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: '#007AFF',
          hover: '#0066D6',
          active: '#0055B3',
          light: '#E6F1FB',
          lighter: '#F0F7FF'
        },
        page: '#F5F5F7',
        card: '#FFFFFF',
        hover: '#F5F5F7',
        active: '#EBEBED',
        ink: {
          primary: '#1D1D1F',
          secondary: '#6E6E73',
          tertiary: '#AEAEB2',
          inverse: '#FFFFFF'
        },
        line: {
          DEFAULT: '#E5E5EA',
          hover: '#D1D1D6'
        },
        success: { DEFAULT: '#34C759', light: '#E8F8EC' },
        warning: { DEFAULT: '#FF9500', light: '#FFF4E6' },
        danger: { DEFAULT: '#FF3B30', light: '#FFEBE8' },
        subject: { DEFAULT: '#3B82F6', light: '#EBF3FF' },
        analysis: { DEFAULT: '#10B981', light: '#E8F8F0' },
        // 错题本 8 色
        tag: {
          blue: '#007AFF',
          green: '#34C759',
          orange: '#FF9500',
          purple: '#AF52DE',
          pink: '#FF2D92',
          cyan: '#5AC8FA',
          amber: '#FFB340',
          indigo: '#5856D6'
        }
      },
      fontFamily: {
        sans: [
          'PingFang SC', 'SF Pro Text', '-apple-system', 'BlinkMacSystemFont',
          'Segoe UI', 'sans-serif'
        ],
        mono: ['SF Mono', 'Fira Code', 'Cascadia Code', 'monospace']
      },
      fontSize: {
        h1: ['28px', { lineHeight: '1.3', fontWeight: '600', letterSpacing: '-0.02em' }],
        h2: ['20px', { lineHeight: '1.4', fontWeight: '600' }],
        h3: ['16px', { lineHeight: '1.5', fontWeight: '600' }],
        body: ['14px', { lineHeight: '1.5' }],
        caption: ['12px', { lineHeight: '1.5' }],
        code: ['13px', { lineHeight: '1.6' }]
      },
      borderRadius: {
        sm: '6px',
        md: '8px',
        lg: '12px',
        full: '9999px'
      },
      spacing: {
        xs: '4px',
        sm: '8px',
        md: '12px',
        lg: '16px',
        xl: '24px',
        '2xl': '32px',
        '3xl': '48px'
      },
      maxWidth: {
        content: '1200px',
        contentWide: '1320px'
      },
      boxShadow: {
        // 设计系统唯一允许的阴影：输入框聚焦环
        focus: '0 0 0 3px rgba(0,122,255,0.12)'
      },
      transitionProperty: {
        DEFAULT: 'all'
      }
    }
  },
  plugins: [],

  // 全局禁用默认阴影，强制无阴影设计语言
  corePlugins: {
    boxShadow: true
  }
}
