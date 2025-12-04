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
  menuItem: MenuItem;
  quantity: number;
  unitPrice: number;
  customizations?: string;
}

export interface Order {
  id: number;
  items: OrderItem[];
  status: OrderStatus;
  createdAt: string;
  totalAmount: number;
}

export enum OrderStatus {
  PENDING = "pending",
  CONFIRMED = 'confirmed',
  PAID = 'paid',
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
  paidAt: string;
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

