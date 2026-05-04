<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Http;

class KitchenController extends Controller
{
    private string $baseUrl;
    private array  $internalHeaders;

    public function __construct()
    {
        $this->baseUrl = config('services.kitchen.url');
        $this->internalHeaders = [
            'X-Internal-Secret' => env('INTERNAL_SECRET'),
            'Accept'            => 'application/json',
            'Content-Type'      => 'application/json',
        ];
    }

    // GET /api/kitchen/queue
    public function getQueue()
    {
        try {
            $response = Http::withHeaders($this->internalHeaders)
                ->timeout(5)
                ->get("{$this->baseUrl}/api/kitchen/queue");

            return response()->json($response->json(), $response->status());
        } catch (\Exception $e) {
            return response()->json(['message' => 'Kitchen Service no disponible.'], 503);
        }
    }

    // GET /api/kitchen/history
    public function getHistory()
    {
        try {
            $response = Http::withHeaders($this->internalHeaders)
                ->timeout(5)
                ->get("{$this->baseUrl}/api/kitchen/history");

            return response()->json($response->json(), $response->status());
        } catch (\Exception $e) {
            return response()->json(['message' => 'Kitchen Service no disponible.'], 503);
        }
    }

    // POST /api/kitchen/orders
    public function receiveOrder(Request $request)
    {
        $request->validate([
            'order_id' => 'required|string',
            'kiosk_id' => 'required|string',
            'items'    => 'required|array|min:1',
            'total'    => 'required|numeric',
        ]);

        try {
            $response = Http::withHeaders($this->internalHeaders)
                ->timeout(5)
                ->post("{$this->baseUrl}/api/kitchen/orders", $request->all());

            return response()->json($response->json(), $response->status());
        } catch (\Exception $e) {
            return response()->json(['message' => 'Kitchen Service no disponible.'], 503);
        }
    }

    // PATCH /api/kitchen/orders/{order_id}/start
    public function startOrder(string $order_id)
    {
        try {
            $response = Http::withHeaders($this->internalHeaders)
                ->timeout(5)
                ->patch("{$this->baseUrl}/api/kitchen/orders/{$order_id}/start");

            return response()->json($response->json(), $response->status());
        } catch (\Exception $e) {
            return response()->json(['message' => 'Kitchen Service no disponible.'], 503);
        }
    }

    // PATCH /api/kitchen/orders/{order_id}/complete
    public function completeOrder(string $order_id)
    {
        try {
            $response = Http::withHeaders($this->internalHeaders)
                ->timeout(5)
                ->patch("{$this->baseUrl}/api/kitchen/orders/{$order_id}/complete");

            return response()->json($response->json(), $response->status());
        } catch (\Exception $e) {
            return response()->json(['message' => 'Kitchen Service no disponible.'], 503);
        }
    }

    // PATCH /api/kitchen/orders/{order_id}/items/{item_id}/toggle
    public function toggleItem(string $order_id, int $item_id)
    {
        try {
            $response = Http::withHeaders($this->internalHeaders)
                ->timeout(5)
                ->patch("{$this->baseUrl}/api/kitchen/orders/{$order_id}/items/{$item_id}/toggle");

            return response()->json($response->json(), $response->status());
        } catch (\Exception $e) {
            return response()->json(['message' => 'Kitchen Service no disponible.'], 503);
        }
    }

    public function sync()
    {
        try {
            $response = Http::withHeaders($this->internalHeaders)
                ->timeout(5)
                ->post("{$this->baseUrl}/api/kitchen/sync");

            return response()->json($response->json(), $response->status());
        } catch (\Exception $e) {
            return response()->json(['message' => 'Kitchen Service no disponible.'], 503);
        }
    }
}