import apiClient from './api';
import * as Types from '../types/index';
import { Payment } from '../types/index';

class CashierAppController {
  // List all pending counter payments
  async listPendingCounterPayments(): Promise<Types.Order[]> {
    try {
      const response = await apiClient.get<Types.ApiResponse<Types.Order[]>>(
        '/orders/counter-confirmed'
      );
      
      if (response.data.data) {
        return response.data.data;
      }
      
      return [];
    } catch (error: any) {
      console.error('Error listing pending counter payments:', error);
      throw new Error(error.response?.data?.message || 'Failed to load pending payments');
    }
  }

  // Find order by order number
  async findOrder(orderID: number): Promise<Types.Order> {
    try {
      const response = await apiClient.get<Types.ApiResponse<Types.Order>>(
        `/orders/${encodeURIComponent(orderID)}`
      );
      
      if (response.data.data) {
        return response.data.data;
      }
      
      throw new Error('Order not found');
    } catch (error: any) {
      console.error('Error finding order:', error);
      throw new Error(error.response?.data?.message || 'Failed to find order');
    }
  }

  // Complete counter payment for an order
  async completeCounterPayment(
    orderID: number,
    paymentMethod: string
  ): Promise<Payment> {
    try {
      const response = await apiClient.post<Types.ApiResponse<Payment>>(
        `/payments/process-counter`,
        { payment_method: paymentMethod , order_id: orderID }
      );
      
      if (response.data.data) {
        return response.data.data;
      }
      
      throw new Error('Failed to complete payment: No payment data returned');
    } catch (error: any) {
      console.error('Error completing counter payment:', error);
      throw new Error(error.response?.data?.message || 'Failed to complete payment');
    }
  }
}

export const cashierAppController = new CashierAppController();
export default CashierAppController;
