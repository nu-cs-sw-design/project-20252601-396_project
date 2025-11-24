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
  quantity: number;
  specialInstructions?: string;
}

export interface Order {
  id: string;
  items: OrderItem[];
  total: number;
  status: OrderStatus;
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

// API Response Types
export interface ApiResponse<T = any> {
  status: string;
  message?: string;
  data?: T;
}

