import apiClient from './api';
import * as Types from '../types/index';

class KitchenAppController {
  // Get order queue
  async getOrderQueue(): Promise<Types.Order[]> {
    try {
      const response = await apiClient.get<Types.ApiResponse<Types.Order[]>>(
        '/kitchen/order-queue'
      );
      
      if (response.data.data) {
        return response.data.data;
      }
      
      return [];
    } catch (error: any) {
      console.error('Error getting order queue:', error);
      throw new Error(error.response?.data?.message || 'Failed to load order queue');
    }
  }

  // Mark order as in preparation
  async markInPreparation(orderID: number): Promise<void> {
    try {
      await apiClient.put<Types.ApiResponse<void>>(
        `/kitchen/update-order-status/${orderID}`,
        { status: Types.OrderStatus.PREPARING }
      );
    } catch (error: any) {
      console.error('Error marking order in preparation:', error);
      throw new Error(error.response?.data?.message || 'Failed to update order status');
    }
  }

  // Mark order as ready
  async markReady(orderID: number): Promise<void> {
    try {
      await apiClient.put<Types.ApiResponse<void>>(
        `/kitchen/update-order-status/${orderID}`,
        { status: Types.OrderStatus.READY }
      );
    } catch (error: any) {
      console.error('Error marking order as ready:', error);
      throw new Error(error.response?.data?.message || 'Failed to update order status');
    }
  }

  // Cancel an order
  async cancelOrder(orderID: number): Promise<void> {
    try {
      await apiClient.delete<Types.ApiResponse<void>>(
        `/kitchen/orders/${orderID}`
      );
    } catch (error: any) {
      console.error('Error cancelling order:', error);
      throw new Error(error.response?.data?.message || 'Failed to cancel order');
    }
  }
}

export const kitchenAppController = new KitchenAppController();
export default KitchenAppController;
