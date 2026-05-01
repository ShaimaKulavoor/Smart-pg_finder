import React from 'react';

export const SkeletonCard = () => {
  return (
    <div className="bg-white rounded-lg shadow-lg overflow-hidden">
      {/* Image Skeleton */}
      <div className="w-full h-48 bg-gray-300 animate-shimmer"></div>

      {/* Content Skeleton */}
      <div className="p-5 space-y-4">
        {/* Title Skeleton */}
        <div className="h-6 bg-gray-300 rounded animate-shimmer w-3/4"></div>

        {/* Location Skeleton */}
        <div className="h-4 bg-gray-300 rounded animate-shimmer w-1/2"></div>

        {/* Price Skeleton */}
        <div className="space-y-2">
          <div className="h-8 bg-gray-300 rounded animate-shimmer w-1/3"></div>
          <div className="h-4 bg-gray-300 rounded animate-shimmer w-1/4"></div>
        </div>

        {/* Details Grid Skeleton */}
        <div className="grid grid-cols-3 gap-2 pt-4 border-t">
          <div className="h-6 bg-gray-300 rounded animate-shimmer"></div>
          <div className="h-6 bg-gray-300 rounded animate-shimmer"></div>
          <div className="h-6 bg-gray-300 rounded animate-shimmer"></div>
        </div>

        {/* Tags Skeleton */}
        <div className="flex gap-2 pt-4">
          <div className="h-6 bg-gray-300 rounded-full animate-shimmer w-24"></div>
          <div className="h-6 bg-gray-300 rounded-full animate-shimmer w-24"></div>
        </div>

        {/* Button Skeleton */}
        <div className="h-10 bg-gray-300 rounded-lg animate-shimmer w-full mt-4"></div>
      </div>
    </div>
  );
};

export const SkeletonLoader = ({ count = 6 }) => {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      {Array.from({ length: count }).map((_, index) => (
        <SkeletonCard key={index} />
      ))}
    </div>
  );
};

export const SkeletonSearchForm = () => {
  return (
    <div className="bg-white rounded-lg shadow-2xl p-8 space-y-6">
      {/* Search Row */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {Array.from({ length: 3 }).map((_, index) => (
          <div key={index} className="space-y-2">
            <div className="h-4 bg-gray-300 rounded animate-shimmer w-1/3"></div>
            <div className="h-10 bg-gray-300 rounded animate-shimmer"></div>
          </div>
        ))}
      </div>

      {/* Additional Info Row */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {Array.from({ length: 3 }).map((_, index) => (
          <div key={index} className="space-y-2">
            <div className="h-4 bg-gray-300 rounded animate-shimmer w-1/3"></div>
            <div className="h-10 bg-gray-300 rounded animate-shimmer"></div>
          </div>
        ))}
      </div>

      {/* Button */}
      <div className="h-12 bg-gray-300 rounded-lg animate-shimmer w-full"></div>
    </div>
  );
};

export const SkeletonDetailsPage = () => {
  return (
    <div className="space-y-6">
      {/* Image */}
      <div className="w-full h-96 bg-gray-300 rounded-lg animate-shimmer"></div>

      {/* Title and Info */}
      <div className="space-y-3">
        <div className="h-8 bg-gray-300 rounded animate-shimmer w-2/3"></div>
        <div className="h-4 bg-gray-300 rounded animate-shimmer w-1/3"></div>
      </div>

      {/* Details Grid */}
      <div className="grid grid-cols-3 gap-4">
        {Array.from({ length: 3 }).map((_, index) => (
          <div key={index} className="bg-gray-300 h-20 rounded animate-shimmer"></div>
        ))}
      </div>

      {/* Description */}
      <div className="space-y-2">
        <div className="h-4 bg-gray-300 rounded animate-shimmer"></div>
        <div className="h-4 bg-gray-300 rounded animate-shimmer"></div>
        <div className="h-4 bg-gray-300 rounded animate-shimmer w-3/4"></div>
      </div>
    </div>
  );
};
