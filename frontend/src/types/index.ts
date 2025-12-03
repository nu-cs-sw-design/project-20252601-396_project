/**
 * Type definitions for the Fast Food Ordering System
 */

// Menu Item Types
export interface MenuItem {
  id: string;
  name: string;
  price: number;
  category: string;
  description: string;
}

// Order Types
export interface OrderItem {
  menuItemId: string;
  menuItem?: MenuItem;
  quantity: number;
  unitPrice: number;
  customizations?: string;
  specialInstructions?: string;
}

export interface Order {
  id: string;
  orderNumber: string;
  items: OrderItem[];
  total: number;
  status: OrderStatus;
  paymentStatus: PaymentStatus | string;
  createdAt: string;
  customerName?: string;
  customerEmail?: string;
}

export enum OrderStatus {
  PENDING = 'pending',
  CONFIRMED = 'confirmed',
  PREPARING = 'preparing',
  READY = 'ready',
  COMPLETED = 'completed',
  CANCELLED = 'cancelled',
}

// Payment Types
export interface Payment {
  id: string;
  orderId: string;
  amount: number;
  method: string;
  status: PaymentStatus;
  paidAt: string;
}

export enum PaymentStatus {
  PENDING = 'pending',
  COMPLETED = 'completed',
  FAILED = 'failed'
}

// Daily Sales Summary Types
export interface DailySalesSummary {
  date: string;
  totalRevenue: number;
  numberOfOrders: number;
  topSellingItems: MenuItem[];
}

// API Response Types
export interface ApiResponse<T = any> {
  status: string;
  message?: string;
  data?: T;
}

