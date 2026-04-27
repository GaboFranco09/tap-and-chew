<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Http;

class MenuController extends Controller
{
    private string $baseUrl;
    private array  $internalHeaders;

    public function __construct()
    {
        $this->baseUrl = config('services.menu.url');
        $this->internalHeaders = [
            'X-Internal-Secret' => env('INTERNAL_SECRET'),
            'Accept'            => 'application/json',
        ];
    }

    // GET /api/menu/categories
    public function getCategories()
    {
        try {
            $response = Http::withHeaders($this->internalHeaders)
                ->timeout(5)
                ->get("{$this->baseUrl}/api/menu/categories/");

            return response()->json($response->json(), $response->status());
        } catch (\Exception $e) {
            return response()->json(['message' => 'Menu Service no disponible.'], 503);
        }
    }

    // GET /api/menu/categories/active
    public function getActiveCategories()
    {
        try {
            $response = Http::withHeaders($this->internalHeaders)
                ->timeout(5)
                ->get("{$this->baseUrl}/api/menu/categories/active/");

            return response()->json($response->json(), $response->status());
        } catch (\Exception $e) {
            return response()->json(['message' => 'Menu Service no disponible.'], 503);
        }
    }

    // POST /api/menu/categories
    public function createCategory(Request $request)
    {
        $request->validate([
            'name' => 'required|string|max:100',
        ]);

        try {
            $response = Http::withHeaders($this->internalHeaders)
                ->timeout(5)
                ->post("{$this->baseUrl}/api/menu/categories/", $request->all());

            return response()->json($response->json(), $response->status());
        } catch (\Exception $e) {
            return response()->json(['message' => 'Menu Service no disponible.'], 503);
        }
    }

    // GET /api/menu/products
    public function getProducts(Request $request)
    {
        try {
            $query    = $request->getQueryString();
            $url      = "{$this->baseUrl}/api/menu/products/" . ($query ? "?{$query}" : '');
            $response = Http::withHeaders($this->internalHeaders)
                ->timeout(5)
                ->get($url);

            return response()->json($response->json(), $response->status());
        } catch (\Exception $e) {
            return response()->json(['message' => 'Menu Service no disponible.'], 503);
        }
    }

    // GET /api/menu/products/available
    public function getAvailableProducts()
    {
        try {
            $response = Http::withHeaders($this->internalHeaders)
                ->timeout(5)
                ->get("{$this->baseUrl}/api/menu/products/available/");

            return response()->json($response->json(), $response->status());
        } catch (\Exception $e) {
            return response()->json(['message' => 'Menu Service no disponible.'], 503);
        }
    }

    // POST /api/menu/products
    public function createProduct(Request $request)
    {
        $request->validate([
            'name'        => 'required|string|max:150',
            'price'       => 'required|numeric|min:0',
            'category_id' => 'required|integer',
        ]);

        try {
            $response = Http::withHeaders($this->internalHeaders)
                ->timeout(5)
                ->post("{$this->baseUrl}/api/menu/products/", $request->all());

            return response()->json($response->json(), $response->status());
        } catch (\Exception $e) {
            return response()->json(['message' => 'Menu Service no disponible.'], 503);
        }
    }

    // GET /api/menu/combos
    public function getCombos()
    {
        try {
            $response = Http::withHeaders($this->internalHeaders)
                ->timeout(5)
                ->get("{$this->baseUrl}/api/menu/combos/");

            return response()->json($response->json(), $response->status());
        } catch (\Exception $e) {
            return response()->json(['message' => 'Menu Service no disponible.'], 503);
        }
    }

    // GET /api/menu/combos/active
    public function getActiveCombos()
    {
        try {
            $response = Http::withHeaders($this->internalHeaders)
                ->timeout(5)
                ->get("{$this->baseUrl}/api/menu/combos/active/");

            return response()->json($response->json(), $response->status());
        } catch (\Exception $e) {
            return response()->json(['message' => 'Menu Service no disponible.'], 503);
        }
    }
}